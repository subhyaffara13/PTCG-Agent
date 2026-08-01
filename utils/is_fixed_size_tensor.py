
def is_fixed_size_tensor(value: onnx.ValueInfoProto):
    """
    Check if value is a tensor with a fixed shape.
    :param value: onnx.ValueInfoProto to check
    :return: True if value is a tensor, with a shape, where all dimensions have fixed values.
    """

    is_fixed = False
    if value.type.HasField("tensor_type"):
        shape = value.type.tensor_type.shape
        if shape:
            is_fixed = True  # scalar has no dims so set to True and unset if we hit a dim without a valid value
            for dim in shape.dim:
                if dim.HasField("dim_value") and dim.dim_value > 0:
                    continue

                # anything else means it's a dynamic value
                is_fixed = False
                break

    return is_fixed

