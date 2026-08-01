
def class_has_getattribute(cls: type) -> bool:
    try:
        if isinstance(
            inspect.getattr_static(cls, "__getattribute__"),
            types.FunctionType,
        ):
            return True
    except AttributeError:
        pass
    return False

