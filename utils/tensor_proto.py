
def tensor_proto(tag, tensor):
    """Outputs a `Summary` protocol buffer containing the full tensor.
    The generated Summary has a Tensor.proto containing the input Tensor.
    Args:
      tag: A name for the generated node. Will also serve as the series name in
        TensorBoard.
      tensor: Tensor to be converted to protobuf
    Returns:
      A tensor protobuf in a `Summary` protobuf.
    Raises:
      ValueError: If tensor is too big to be converted to protobuf, or
                     tensor data type is not supported
    """
    if tensor.numel() * tensor.itemsize >= (1 << 31):
        raise ValueError(
            "tensor is bigger than protocol buffer's hard limit of 2GB in size"
        )

    if tensor.dtype in _TENSOR_TYPE_MAP:
        dtype, field_name, conversion_fn = _TENSOR_TYPE_MAP[tensor.dtype]
        tensor_proto = TensorProto(
            **{
                "dtype": dtype,
                "tensor_shape": TensorShapeProto(
                    dim=[TensorShapeProto.Dim(size=x) for x in tensor.shape]
                ),
                field_name: conversion_fn(tensor),
            },
        )
    else:
        raise ValueError(f"{tag} has unsupported tensor dtype {tensor.dtype}")

    plugin_data = SummaryMetadata.PluginData(plugin_name="tensor")
    smd = SummaryMetadata(plugin_data=plugin_data)
    return Summary(value=[Summary.Value(tag=tag, metadata=smd, tensor=tensor_proto)])

