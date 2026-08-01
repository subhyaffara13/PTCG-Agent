
def _should_repr_global_name(obj: object) -> bool:
    if callable(obj):
        # For pytest fixtures the __repr__ method provides more information than the function name.
        return isinstance(obj, FixtureFunctionDefinition)

    try:
        return not hasattr(obj, "__name__")
    except Exception:
        return True

