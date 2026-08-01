
def tensor_size(array):
    """
    Framework-agnostic version of size operation.
    """
    if is_numpy_array(array):
        return np.size(array)
    elif is_torch_tensor(array):
        return array.numel()
    else:
        raise ValueError(f"Type not supported for tensor_size: {type(array)}.")


def tensor_size(op_type, dims):
    ITEM_SIZES = {
        NNAPI_OperandCode.TENSOR_FLOAT32: 4,
        NNAPI_OperandCode.TENSOR_INT32: 4,
        NNAPI_OperandCode.TENSOR_QUANT8_ASYMM: 1,
        NNAPI_OperandCode.TENSOR_QUANT16_SYMM: 2,
        NNAPI_OperandCode.TENSOR_QUANT16_ASYMM: 2,
    }
    size = ITEM_SIZES[op_type]
    for d in dims:
        size *= d
    return size

