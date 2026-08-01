
def _get_restore_parameters(
    directory: epath.Path,
    item: Optional[PyTree],
    structure: PyTree,
    param_names: Optional[PyTree],
    transforms: Optional[PyTree],
    restore_args: Optional[PyTree],
    pytree_metadata_options: tree_metadata.PyTreeMetadataOptions,
    byte_limiter: Optional[LimitInFlightBytes] = None,
    transforms_default_to_original: bool = True,
    use_zarr3: bool = False,
    partial_restore: bool = False,
) -> Tuple[PyTree, PyTree]:
  """Construct parameters needed for restoration.

  If transforms are not provided, the method is pretty simple: param_infos are
  constructed from the structure of the original checkpoint, and restore_args
  are serialized to a tree structure compatible with param_infos and structure.

  If transforms are provided, things become more complicated because we must
  determine exactly which parameters the user desires to restore, and construct
  param_infos and restore_args for these, while discarding unneeded parameters.
  In essence, the process can be thought of as reversing the transformations.
  This happens differently for different types of transforms.
  1. Renamed key: Identify the original key name (in the checkpoint) and carry
    over the provided restore args for the parameter.
  2. multi_value_fn: Users are required to specify multi_value_fn_input_args.
    Any keys named here must be loaded, and their restore args are also given
    here.
  3. Unspecified key: A key which is unspecified in the transforms but present
    in the `item` is a key that is carried over from the checkpoint unchanged.
  4. Fallback key: This is a key that is present in the `item` but not in the
    original checkpoint. It does not need to be restored.
  5. Keys present in the original checkpoint but not in the `item`/`transforms`
    are implicitly ignored, and not restored.

  Args:
    directory: Checkpoint directory.
    item: Optional reference item.
    structure: The structure of the original checkpoint.
    param_names: Tree of parameter names.
    transforms: User-provided transformations. If None, they were not provided.
      Has the structure of the desired output tree.
    restore_args: User-provided restoration arguments. If None, they were not
      provided. Otherwise, the tree has the same structure as the desired output
      tree.
    pytree_metadata_options: `PyTreeMetadataOptions` to manage metadata.
    byte_limiter: A LimitInFlightBytes object.
    transforms_default_to_original: See transform_utils.apply_transformations.
    use_zarr3: If True, use Zarr ver3 otherwise Zarr ver2
    partial_restore: If True, only restore the parameters present in structure.

  Returns:
    Tuple of param_infos, and restore_args.
  """
  flat_structure = tree_utils.to_flat_dict(structure, keep_empty_nodes=True)
  if param_names is None:
    param_names = get_param_names(structure)
  flat_param_names = tree_utils.to_flat_dict(param_names, keep_empty_nodes=True)
  if restore_args is None:
    restore_args = jax.tree.map(lambda x: RestoreArgs(), structure)
  flat_restore_args = tree_utils.to_flat_dict(
      restore_args, keep_empty_nodes=True
  )
  flat_item = tree_utils.to_flat_dict(item, keep_empty_nodes=True)
  flat_param_infos = {}
  flat_input_restore_args = {}
  is_ocdbt_checkpoint = type_handlers.is_ocdbt_checkpoint(directory)
  ts_context = ts_utils.get_ts_context(use_ocdbt=is_ocdbt_checkpoint)

  def _get_param_info(
      name: str,
      meta_or_value: Union[Any, tree_metadata.ValueMetadataEntry],
  ) -> Union[ParamInfo, Any]:
    if empty_values.is_supported_empty_value(
        meta_or_value, pytree_metadata_options
    ):
      # Empty node, ParamInfo should not be returned.
      return meta_or_value
    elif not isinstance(meta_or_value, tree_metadata.ValueMetadataEntry):
      # Aggregated value.
      skip_deserialize = True
    else:
      skip_deserialize = meta_or_value.skip_deserialize
    return ParamInfo(
        name=name,
        parent_dir=directory,
        skip_deserialize=skip_deserialize,
        is_ocdbt_checkpoint=is_ocdbt_checkpoint,
        byte_limiter=byte_limiter,
        use_zarr3=use_zarr3,
        ts_context=ts_context,
        # Skip raising array data missing error on this code path, since it
        # almost exclusively handles legacy use cases.
        raise_array_data_missing_error=False,
    )

  if partial_restore:
    for key, meta in flat_structure.items():
      if key not in flat_item:
        flat_param_infos[key] = ParamInfo(
            name='', parent_dir=directory, skip_deserialize=True
        )
        flat_input_restore_args[key] = RestoreArgs()
      else:
        flat_param_infos[key] = _get_param_info(flat_param_names[key], meta)
        flat_input_restore_args[key] = flat_restore_args[key]
    restore_args = tree_utils.from_flat_dict(
        flat_input_restore_args, target=structure
    )
  elif transforms is None:
    for key, meta in flat_structure.items():
      flat_param_infos[key] = _get_param_info(flat_param_names[key], meta)
    restore_args = tree_metadata.serialize_tree(
        restore_args, pytree_metadata_options
    )
  else:
    if item is None:
      raise ValueError(
          'If providing `transforms`, must provide `item` matching structure'
          ' of expected result.'
      )
    flat_transforms = tree_utils.to_flat_dict(transforms)

    for input_key, meta in flat_structure.items():
      maybe_input_args = _find_matching_input_args(
          input_key, flat_item, flat_transforms, flat_restore_args
      )
      if maybe_input_args:
        flat_param_infos[input_key] = _get_param_info(
            flat_param_names[input_key], meta
        )
        flat_input_restore_args[input_key] = maybe_input_args
      elif input_key in flat_item and input_key in flat_structure:
        # Key is present in both input and output.
        if _has_use_fallback_transform(input_key, flat_transforms):
          # Indicates that a `use_fallback` transformation was specified.
          if transforms_default_to_original:
            # Specified `use_fallback`, but key was also present in the
            # checkpoint. This means we should skip loading, since it will be
            # overridden with a new value.
            flat_param_infos[input_key] = ParamInfo(
                name='', parent_dir=directory, skip_deserialize=True
            )
            flat_input_restore_args[input_key] = RestoreArgs()
          else:
            # Specified `use_fallback`, but `transforms_default_to_original`
            # is False. This means we draw the value from the user-provided
            # `item`.
            flat_param_infos[input_key] = _get_param_info(
                flat_param_names[input_key], meta
            )
            flat_input_restore_args[input_key] = flat_restore_args[input_key]
        else:
          # Transform not specified.
          if transforms_default_to_original:
            # Key/value is carried over from the original unchanged.
            flat_param_infos[input_key] = _get_param_info(
                flat_param_names[input_key], meta
            )
            flat_input_restore_args[input_key] = flat_restore_args[input_key]
          else:
            # Take the value from the user-provided `item`, ignoring any value
            # in the checkpoint.
            flat_param_infos[input_key] = ParamInfo(
                name='', parent_dir=directory, skip_deserialize=True
            )
            flat_input_restore_args[input_key] = RestoreArgs()
      else:
        # No match, restoration not required since it will be dropped from the
        # output.
        flat_param_infos[input_key] = ParamInfo(
            name='', parent_dir=directory, skip_deserialize=True
        )
        flat_input_restore_args[input_key] = RestoreArgs()

    restore_args = tree_utils.from_flat_dict(
        flat_input_restore_args, target=structure
    )

  return (
      tree_utils.from_flat_dict(flat_param_infos, target=structure),
      restore_args,
  )

