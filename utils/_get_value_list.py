
def _get_value_list(
    sequence_or_array_attr: _Union[_Sequence[any], ArrayAttr]
) -> _Sequence[any]:
    return [_get_value_or_attribute_value(v) for v in sequence_or_array_attr]

