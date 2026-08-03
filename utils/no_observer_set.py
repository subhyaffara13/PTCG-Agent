from typing import Any

def no_observer_set() -> set[Any]:
    r"""These modules cannot have observers inserted by default."""
    no_observers = {nn.quantizable.LSTM, nn.quantizable.MultiheadAttention}
    return no_observers

