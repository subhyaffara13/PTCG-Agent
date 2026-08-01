
def mesh(
    tag, vertices, colors, faces, config_dict, display_name=None, description=None
):
    """Output a merged `Summary` protocol buffer with a mesh/point cloud.

    Args:
      tag: A name for this summary operation.
      vertices: Tensor of shape `[dim_1, ..., dim_n, 3]` representing the 3D
        coordinates of vertices.
      faces: Tensor of shape `[dim_1, ..., dim_n, 3]` containing indices of
        vertices within each triangle.
      colors: Tensor of shape `[dim_1, ..., dim_n, 3]` containing colors for each
        vertex.
      display_name: If set, will be used as the display name in TensorBoard.
        Defaults to `name`.
      description: A longform readable description of the summary data. Markdown
        is supported.
      config_dict: Dictionary with ThreeJS classes names and configuration.

    Returns:
      Merged summary for mesh/point cloud representation.
    """
    from tensorboard.plugins.mesh import metadata
    from tensorboard.plugins.mesh.plugin_data_pb2 import MeshPluginData

    json_config = _get_json_config(config_dict)

    summaries = []
    tensors = [
        (vertices, MeshPluginData.VERTEX),
        (faces, MeshPluginData.FACE),
        (colors, MeshPluginData.COLOR),
    ]
    tensors = [tensor for tensor in tensors if tensor[0] is not None]
    components = metadata.get_components_bitmask(
        [content_type for (tensor, content_type) in tensors]
    )

    for tensor, content_type in tensors:
        summaries.append(
            _get_tensor_summary(
                tag,
                display_name,
                description,
                tensor,
                content_type,
                components,
                json_config,
            )
        )

    return Summary(value=summaries)


def mesh(sym_name: _Union[str, _ods_ir.StringAttr], mesh: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MeshOp:
  return MeshOp(sym_name=sym_name, mesh=mesh, loc=loc, ip=ip)

