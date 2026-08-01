
def _get_value_or_attribute_value(
    value_or_attr: _Union[any, Attribute, ArrayAttr]
) -> any:
    if isinstance(value_or_attr, Attribute) and hasattr(value_or_attr, "value"):
        return value_or_attr.value
    if isinstance(value_or_attr, ArrayAttr):
        return _get_value_list(value_or_attr)
    return value_or_attr

