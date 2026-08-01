
def _numpy_function_ids() -> dict[int, str]:
    unsupported_funcs = {
        "seed",
        "ranf",
        "get_bit_generator",
        "RandomState",
        "set_bit_generator",
        "sample",
    }

    def is_supported(k: str, v: Any, mod: Any) -> bool:
        if not callable(v):
            return False
        if not getattr(v, "__module__", None):
            return True
        if v.__module__ == mod.__name__:
            return True
        if (
            v.__module__ == "numpy.random.mtrand"
            and mod.__name__ == "numpy.random"
            and k not in unsupported_funcs
        ):
            return True
        return False

    rv = {}
    for mod in NP_SUPPORTED_MODULES:
        for k, v in mod.__dict__.items():
            if is_supported(k, v, mod):
                rv[id(v)] = f"{mod.__name__}.{k}"
    return rv

