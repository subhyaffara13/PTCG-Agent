
def _setattr_with_converter(
    attr_name: str, value_var: str, has_on_setattr: bool, converter: Converter
) -> str:
    """
    Use the cached object.setattr to set *attr_name* to *value_var*, but run
    its converter first.
    """
    return f"_setattr('{attr_name}', {converter._fmt_converter_call(attr_name, value_var)})"

