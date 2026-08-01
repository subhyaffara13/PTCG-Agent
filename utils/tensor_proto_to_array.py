
def tensor_proto_to_array(initializer: TensorProto) -> numpy.ndarray:
    if initializer.data_type in (onnx_proto.TensorProto.FLOAT, onnx_proto.TensorProto.FLOAT16):
        return onnx.numpy_helper.to_array(initializer)

    raise ValueError(
        f"Only float type is supported. Weights {initializer.name} is {type_to_name[initializer.data_type]}"
    )

