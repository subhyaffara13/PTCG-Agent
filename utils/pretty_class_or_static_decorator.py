
def pretty_class_or_static_decorator(tp: CallableType) -> str | None:
    """Return @classmethod or @staticmethod, if any, for the given callable type."""
    definition = get_func_def(tp)
    if definition is not None and isinstance(definition, SYMBOL_FUNCBASE_TYPES):
        if definition.is_class:
            return "@classmethod"
        if definition.is_static:
            return "@staticmethod"
    return None

