
def quantize_nparray(qType, arr, scale, zero_point, low=None, high=None):
    assert qType in ONNX_TYPE_TO_NP_TYPE, (
        f"Unexpected data type {qType} requested. Only INT8, UINT8, INT16, and UINT16 are supported."
    )
    if qType in (
        onnx_proto.TensorProto.FLOAT8E4M3FN,
        onnx_proto.TensorProto.FLOAT8E4M3FNUZ,
        onnx_proto.TensorProto.FLOAT8E5M2,
        onnx_proto.TensorProto.FLOAT8E5M2FNUZ,
    ):
        if zero_point != 0:
            raise NotImplementedError(f"zero_point is expected to be null for float 8 not {zero_point!r}.")
        if arr.dtype == numpy.float32:
            onnx_type = TensorProto.FLOAT
        elif arr.dtype == numpy.float16:
            onnx_type = TensorProto.FLOAT16
        else:
            raise ValueError(f"Unexpected dtype {arr.dtype}.")
        onnx_model = make_model(
            make_graph(
                [
                    make_node(
                        "Constant", [], ["zero_point"], value=onnx.helper.make_tensor("zero_point", qType, [], [0])
                    ),
                    make_node("QuantizeLinear", ["X", "scale", "zero_point"], ["Y"]),
                ],
                "qu",
                [
                    make_tensor_value_info("X", onnx_type, None),
                    make_tensor_value_info("scale", onnx_type, None),
                ],
                [make_tensor_value_info("Y", qType, None)],
            )
        )
        ref = ReferenceEvaluator(onnx_model)
        return _check_type(ref.run(None, {"X": arr, "scale": scale})[0])
    else:
        # Quantizes data for all integer types.
        #
        # For int4 types, the quantized data is returned as either np.int8 or np.uint8,
        # which matches the python reference ONNX implementation of QuantizeLinear.
        # This data can be packed into 4-bit elements by using pack_bytes_to_4bit().
        dtype = ONNX_TYPE_TO_NP_TYPE[qType]
        qmin, qmax = get_qmin_qmax_for_qType(qType, reduce_range=False, symmetric=False)

        cliplow = max(qmin, low) if low is not None else qmin
        cliphigh = min(qmax, high) if high is not None else qmax
        arr_fp32 = numpy.asarray((arr.astype(numpy.float32) / scale).round() + zero_point)
        numpy.clip(arr_fp32, cliplow, cliphigh, out=arr_fp32)
        return _check_type(arr_fp32.astype(dtype))

