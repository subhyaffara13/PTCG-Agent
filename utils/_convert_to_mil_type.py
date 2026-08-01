
def _convert_to_mil_type(shape, dtype, name: str):
    mil_shape = shape
    if _check_enumerated_shape(shape):
        mil_shape = ct.EnumeratedShapes(shape)
    ml_type = TensorType(shape=mil_shape, dtype=torch_to_mil_types[dtype])
    ml_type.name = name
    return ml_type

