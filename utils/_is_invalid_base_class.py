
def _is_invalid_base_class(cls: nodes.ClassDef) -> bool:
    return cls.name in INVALID_BASE_CLASSES and is_builtin_object(cls)

