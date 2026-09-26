"""Pytest startup adjustments and shared Connect Four test helpers."""

import importlib
import importlib.util
import pathlib
import sys
import sysconfig
import threading
import time
import types
import typing

import pytest

if typing.TYPE_CHECKING:
    import ConnectFour

def _load_stdlib_code_module() -> None:
    if "code" in sys.modules:
        return

    stdlib_path = pathlib.Path(sysconfig.get_path("stdlib")) / "code.py"
    spec = importlib.util.spec_from_file_location("code", stdlib_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load stdlib code module from {stdlib_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["code"] = module
    spec.loader.exec_module(module)


_load_stdlib_code_module()


class FakeNeoTrellisGame:
    """Fake board implementation used to exercise Connect Four without hardware."""

    CALLBACK_TIMEOUT_SECONDS = 0.5
    PRESS_DELAY_SECONDS = 0.33

    def __init__(self):
        self.callbacks = {}
        self.colors = {}
        self.display_updates = 0
        self.key_states = {}

    def init_hardware(self):
        return None

    def set_cell_color(self, x, y, color):
        self.colors[(x, y)] = color

    def update_display(self):
        self.display_updates += 1

    def clear_board(self):
        self.colors.clear()

    def sync(self):
        return None

    def play_sound(self, *_args, **_kwargs):
        pass

    def set_callback(self, x, y, callback):
        self.callbacks[(x, y)] = callback

    def activate_key(self, x, y, edge, enable=True):
        key_state = self.key_states.setdefault((x, y), {})
        key_state["edge"] = edge
        key_state["enable"] = enable
        key_state[edge] = enable

    def _invoke_callback(self, callback, x: int, y: int, edge) -> None:
        callback_error = []

        def _run_callback() -> None:
            try:
                callback(x, y, edge)
            except Exception as exc:  # pragma: no cover - re-raised on caller thread.
                callback_error.append(exc)

        callback_thread = threading.Thread(target=_run_callback, daemon=True)
        callback_thread.start()
        callback_thread.join(self.CALLBACK_TIMEOUT_SECONDS)

        if callback_thread.is_alive():
            raise TimeoutError(
                f"Callback for ({x}, {y}) did not finish within {self.CALLBACK_TIMEOUT_SECONDS} seconds"
            )

        if callback_error:
            raise callback_error[0]

    def press(self, x: int, y: int) -> bool:
        """Simulate a momentary press by firing FALLING then RISING events."""
        callback = self.callbacks.get((x, y))
        key_state = self.key_states.get((x, y), {})
        if callback is None:
            return False

        falling_edge = getattr(sys.modules["adafruit_neotrellis.neotrellis"].NeoTrellis, "EDGE_FALLING")
        rising_edge = getattr(sys.modules["adafruit_neotrellis.neotrellis"].NeoTrellis, "EDGE_RISING")
        press_handled = False

        if key_state.get(falling_edge, False):
            self._invoke_callback(callback, x, y, falling_edge)
            press_handled = True

        time.sleep(self.PRESS_DELAY_SECONDS)

        if key_state.get(rising_edge, False):
            self._invoke_callback(callback, x, y, rising_edge)
            press_handled = True

        return press_handled

    def color_at(self, x, y):
        return self.colors.get((x, y))


def _install_fake_hardware_modules():
    board_module = types.ModuleType("board")
    setattr(board_module, "SCL", object())
    setattr(board_module, "SDA", object())
    sys.modules["board"] = board_module

    busio_module = types.ModuleType("busio")

    class _FakeI2C:
        def __init__(self, *_args, **_kwargs):
            pass

    setattr(busio_module, "I2C", _FakeI2C)
    sys.modules["busio"] = busio_module
    sys.modules["digitalio"] = types.ModuleType("digitalio")

    adafruit_package = types.ModuleType("adafruit_neotrellis")
    multitrellis_module = types.ModuleType("adafruit_neotrellis.multitrellis")
    neotrellis_module = types.ModuleType("adafruit_neotrellis.neotrellis")

    class _FakeMultiTrellis:
        def __init__(self, *_args, **_kwargs):
            pass

        def color(self, *_args, **_kwargs):
            pass

        def show(self):
            pass

        def sync(self):
            pass

        def set_callback(self, *_args, **_kwargs):
            pass

        def activate_key(self, *_args, **_kwargs):
            pass

    class _FakeNeoTrellis:
        EDGE_RISING = 0 # released
        EDGE_FALLING = 1 # pressed

        def __init__(self, *_args, **_kwargs):
            pass

    setattr(multitrellis_module, "MultiTrellis", _FakeMultiTrellis)
    setattr(neotrellis_module, "NeoTrellis", _FakeNeoTrellis)
    setattr(adafruit_package, "multitrellis", multitrellis_module)
    setattr(adafruit_package, "neotrellis", neotrellis_module)

    sys.modules["adafruit_neotrellis"] = adafruit_package
    sys.modules["adafruit_neotrellis.multitrellis"] = multitrellis_module
    sys.modules["adafruit_neotrellis.neotrellis"] = neotrellis_module


@pytest.fixture(scope="session")
def connect_four_module():
    _install_fake_hardware_modules()

    sys.modules.pop("ConnectFour", None)
    sys.modules.pop("NeoTrellisGame", None)
    return importlib.import_module("ConnectFour")


@pytest.fixture
def game_and_board(connect_four_module) -> typing.Tuple["ConnectFour.ConnectFour", FakeNeoTrellisGame]:
    board = FakeNeoTrellisGame()
    game: ConnectFour.ConnectFour
    game = connect_four_module.ConnectFour(board=board)
    return game, board
