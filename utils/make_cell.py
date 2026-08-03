from typing import Any

def make_cell(val: Any = None) -> types.CellType:
    """Some black magic to create a cell object that usually only exists in a closure"""
    x = val

    def f() -> Any:
        return x

    assert f.__closure__ is not None and len(f.__closure__) == 1
    return f.__closure__[0]

