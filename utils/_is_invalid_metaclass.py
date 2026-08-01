
def _is_invalid_metaclass(metaclass: nodes.ClassDef) -> bool:
    try:
        mro = metaclass.mro()
    except (astroid.DuplicateBasesError, astroid.InconsistentMroError):
        return True
    return not any(is_builtin_object(cls) and cls.name == "type" for cls in mro)

