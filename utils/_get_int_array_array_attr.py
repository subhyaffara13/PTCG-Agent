
def _get_int_array_array_attr(
    values: _Optional[_Union[ArrayAttr, _Sequence[_Union[ArrayAttr, IntOrAttrList]]]]
) -> ArrayAttr:
    """Creates an ArrayAttr of ArrayAttrs of IntegerAttrs.

    The input has to be a collection of a collection of integers, where any
    Python _Sequence and ArrayAttr are admissible collections and Python ints and
    any IntegerAttr are admissible integers. Both levels of collections are
    turned into ArrayAttr; the inner level is turned into IntegerAttrs of i64s.
    If the input is None, an empty ArrayAttr is returned.
    """
    if values is None:
        return None

    # Make sure the outer level is a list.
    values = _get_value_list(values)

    # The inner level is now either invalid or a mixed sequence of ArrayAttrs and
    # Sequences. Make sure the nested values are all lists.
    values = [_get_value_list(nested) for nested in values]

    # Turn each nested list into an ArrayAttr.
    values = [_get_int_array_attr(nested) for nested in values]

    # Turn the outer list into an ArrayAttr.
    return ArrayAttr.get(values)

