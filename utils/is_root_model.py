
def is_root_model(info: TypeInfo) -> bool:
    """Return whether the type info is a root model subclass (or the `RootModel` class itself)."""
    return info.has_base(ROOT_MODEL_FULLNAME)

