
def is_cython_function(obj: object) -> bool:
    return (
        callable(obj)
        and hasattr(type(obj), "__name__")
        and type(obj).__name__ == "cython_function_or_method"
    )

