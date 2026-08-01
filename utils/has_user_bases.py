
def has_user_bases(info: TypeInfo) -> bool:
    return any(base.module_name not in ("builtins", "typing", "enum") for base in info.mro[1:])

