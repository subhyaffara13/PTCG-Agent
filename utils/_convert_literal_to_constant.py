
def _convert_literal_to_constant(value: Union[int, ConstantOp, Value]) -> Value:
    if isinstance(value, int):
        return constant(T.index(), value)
    elif isinstance(value, (ConstantOp, Value)):
        return value
    else:
        raise ValueError(f"Invalid value: {value}")

