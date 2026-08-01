
def _assign_with_converter(
    attr_name: str, value_var: str, has_on_setattr: bool, converter: Converter
) -> str:
    """
    Unless *attr_name* has an on_setattr hook, use normal assignment after
    conversion. Otherwise relegate to _setattr_with_converter.
    """
    if has_on_setattr:
        return _setattr_with_converter(attr_name, value_var, True, converter)

    return f"self.{attr_name} = {converter._fmt_converter_call(attr_name, value_var)}"

