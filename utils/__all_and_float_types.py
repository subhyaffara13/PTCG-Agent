
def __all_and_float_types() -> tuple[tuple[type, ...], tuple[type, ...]]:
    try:
        import numpy as np

        all_types: tuple[type, ...] = (
            np.integer,
            np.floating,
            builtins.int,
            builtins.float,
        )
        float_types: tuple[type, ...] = (np.floating, builtins.float)
    except ModuleNotFoundError:
        all_types = (builtins.int, builtins.float)
        float_types = (builtins.float,)

    return all_types, float_types

