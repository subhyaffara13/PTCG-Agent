from typing import Callable

def fake_signature(fn: Callable[_P, R], nargs: int) -> Callable[_P, R]:
    """FX gets confused by varargs, de-confuse it"""
    argnames = ",".join(f"arg{i}" for i in range(nargs))
    return eval(f"lambda {argnames}: fn({argnames})", {"fn": fn})

