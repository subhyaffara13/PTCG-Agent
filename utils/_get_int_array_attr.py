
def _get_int_array_attr(
    values: _Optional[_Union[ArrayAttr, IntOrAttrList]]
) -> ArrayAttr:
    if values is None:
        return None

    # Turn into a Python list of Python ints.
    values = _get_value_list(values)

    # Make an ArrayAttr of IntegerAttrs out of it.
    return ArrayAttr.get(
        [IntegerAttr.get(IntegerType.get_signless(64), v) for v in values]
    )

