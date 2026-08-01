
def _get_tensor_summary(
    name, display_name, description, tensor, content_type, components, json_config
):
    """Create a tensor summary with summary metadata.

    Args:
      name: Uniquely identifiable name of the summary op. Could be replaced by
        combination of name and type to make it unique even outside of this
        summary.
      display_name: Will be used as the display name in TensorBoard.
        Defaults to `name`.
      description: A longform readable description of the summary data. Markdown
        is supported.
      tensor: Tensor to display in summary.
      content_type: Type of content inside the Tensor.
      components: Bitmask representing present parts (vertices, colors, etc.) that
        belong to the summary.
      json_config: A string, JSON-serialized dictionary of ThreeJS classes
        configuration.

    Returns:
      Tensor summary with metadata.
    """
    import torch
    from tensorboard.plugins.mesh import metadata

    tensor = torch.as_tensor(tensor)

    tensor_metadata = metadata.create_summary_metadata(
        name,
        display_name,
        content_type,
        components,
        tensor.shape,
        description,
        json_config=json_config,
    )

    tensor = TensorProto(
        dtype="DT_FLOAT",
        float_val=tensor.reshape(-1).tolist(),
        tensor_shape=TensorShapeProto(
            dim=[
                TensorShapeProto.Dim(size=tensor.shape[0]),
                TensorShapeProto.Dim(size=tensor.shape[1]),
                TensorShapeProto.Dim(size=tensor.shape[2]),
            ]
        ),
    )

    tensor_summary = Summary.Value(
        tag=metadata.get_instance_name(name, content_type),
        tensor=tensor,
        metadata=tensor_metadata,
    )

    return tensor_summary

