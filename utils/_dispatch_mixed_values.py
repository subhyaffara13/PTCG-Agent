
def _dispatch_mixed_values(
    values: MixedValues,
) -> _Tuple[_List[Value], _Union[Operation, Value, OpView], DenseI64ArrayAttr]:
    dynamic_values = []
    packed_values = None
    static_values = None
    if isinstance(values, ArrayAttr):
        static_values = values
    elif isinstance(values, (Operation, Value, OpView)):
        packed_values = values
    else:
        static_values = []
        for size in values or []:
            if isinstance(size, int):
                static_values.append(size)
            elif isinstance(size, IntegerAttr):
                static_values.append(size.value)
            else:
                static_values.append(ShapedType.get_dynamic_size())
                dynamic_values.append(size)
        static_values = DenseI64ArrayAttr.get(static_values)

    return (dynamic_values, packed_values, static_values)

