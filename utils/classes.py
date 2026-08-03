from typing import Callable

def classes(*klasses) -> Callable:
    """Evaluate if the tipo is a subclass of the klasses."""
    return lambda tipo: issubclass(tipo, klasses)

