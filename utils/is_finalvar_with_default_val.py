
def is_finalvar_with_default_val(type_: Type[Any], val: Any) -> bool:
    return is_finalvar(type_) and val is not Undefined and not isinstance(val, FieldInfo)

