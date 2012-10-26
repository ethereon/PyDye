from contextlib import contextmanager
from .utils import save_graphics_state, restore_graphics_state

@contextmanager
def ContextFrame():
    save_graphics_state()
    yield
    restore_graphics_state()