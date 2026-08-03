from typing import Any, Tuple, Union

def batched_serialization_requests(
    tree: PyTree,
    param_infos: PyTree,
    args: PyTree,
    registry: TypeHandlerRegistry,
) -> BatchRequests:
  """Gets a list of batched serialization or deserialization requests."""
  grouped = {}

  def _group_value(
      keypath: Tuple[Any, ...],
      info: ParamInfo,
      value: Union[Any, tree_metadata.ValueMetadataEntry],
      arg: Union[SaveArgs, RestoreArgs],
  ):
    nonlocal grouped
    tuple_key = tree_utils.tuple_path_from_keypath(keypath)
    if info.skip_deserialize:
      return

    if not isinstance(arg, (SaveArgs, RestoreArgs)):
      if tree_utils.is_empty_node(arg):
        return

    if isinstance(arg, RestoreArgs):
      assert isinstance(value, tree_metadata.ValueMetadataEntry), type(value)
      metadata_restore_type = value.value_type
      requested_restore_type = arg.restore_type or metadata_restore_type
      # TODO(cpgaffney): Add a warning message if the requested_restore_type
      # is not the same as the metadata_restore_type.
      if empty_values.is_empty_typestr(requested_restore_type):
        # Skip deserialization of empty node using TypeHandler.
        return
      type_for_registry_lookup = requested_restore_type
    elif isinstance(arg, SaveArgs):
      # Skip serialization of empty node using TypeHandler.
      if tree_utils.is_empty_node(value):
        return
      type_for_registry_lookup = type(value)
    else:
      raise AssertionError(
          f'Expected `RestoreArgs` or `SaveArgs`. Got {type(arg)}.'
      )

    try:
      handler = registry.get(type_for_registry_lookup)
    except ValueError as e:
      raise ValueError(
          f'TypeHandler lookup failed for: type={type_for_registry_lookup},'
          f' keypath={keypath}, ParamInfo={info}, RestoreArgs={arg},'
          f' value={value}'
      ) from e

    if handler not in grouped:
      grouped[handler] = BatchRequest(handler, [], [], [], [])
    request = grouped[handler]
    grouped[handler] = dataclasses.replace(
        request,
        keys=request.keys + [tuple_key],
        values=request.values + [value],
        infos=request.infos + [info],
        args=request.args + [arg],
    )

  jax.tree_util.tree_map_with_path(
      _group_value,
      param_infos,
      tree,
      args,
  )
  return list(grouped.values())

