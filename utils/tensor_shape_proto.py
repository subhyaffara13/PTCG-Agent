
def tensor_shape_proto(outputsize: Sequence[int]) -> TensorShapeProto:
    """Create an object matching a tensor_shape field.

    Follows https://github.com/tensorflow/tensorboard/blob/master/tensorboard/compat/proto/tensor_shape.proto .
    """
    return TensorShapeProto(dim=[TensorShapeProto.Dim(size=d) for d in outputsize])

