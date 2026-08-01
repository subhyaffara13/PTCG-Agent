
def get_qmin_qmax_for_qType(qType, reduce_range=False, symmetric=False):  # noqa: N802
    """
    Return qmin and qmax, the minimum and maximum value representable by the given qType
    :parameter qType: onnx.onnx_pb.TensorProto.UINT8 or onnx.onnx_pb.TensorProto.UINT8
    :return: qmin, qmax
    """
    if qType == onnx_proto.TensorProto.FLOAT8E4M3FN:
        raise NotImplementedError("This function is not implemented for float 8 as not needed.")

    qrange = None

    if reduce_range:
        qrange = ONNX_INT_TYPE_REDUCED_RANGE.get(qType)
    elif symmetric and qType in ONNX_INT_TYPE_SYMMETRIC_RANGE:
        qrange = ONNX_INT_TYPE_SYMMETRIC_RANGE[qType]
    else:
        qrange = ONNX_INT_TYPE_RANGE.get(qType)

    if not qrange:
        raise ValueError(f"Unexpected data type {qType} requested. Only INT8, UINT8, INT16, and UINT16 are supported.")

    qmin, qmax = qrange
    if qmin > 0 or qmax < 0:
        raise ValueError(
            f"qmin and qmax must meet requirement: qmin <= 0 <= qmax while "
            f"qmin:{qmin}, qmmax:{qmax}, dtype={qmin.dtype}, reduce_range={reduce_range}, "
            f"symmetric={symmetric}, qType={qType}"
        )

    return qrange

