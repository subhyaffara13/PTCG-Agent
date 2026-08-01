
def value_name_to_typestr(name: str, value_name_to_typeinfo: dict):
    "Lookup TypeInfo for value name and convert to a string representing the C++ type."
    type = get_typeinfo(name, value_name_to_typeinfo)
    type_str = FbsTypeInfo.typeinfo_to_str(type)
    return type_str

