
def _value_metadata_tree_for_json_dumps(obj: Any) -> Any:
  """Callback for `simplejson.dumps` to convert a PyTree to JSON object."""
  # Handle ValueMetadataEntry instances.
  if tree_utils.is_empty_or_leaf(obj):
    if (
        _module_and_class_name(obj.__class__)
        == _VALUE_METADATA_ENTRY_MODULE_AND_CLASS
    ):
      return dict(
          category='custom',
          clazz=_VALUE_METADATA_ENTRY_CLAZZ,
          data=obj.to_json(),
      )
    raise ValueError(
        f'Expected ValueMetadataEntry, got metadata pytree leaf: {obj}'
    )

  # Check namedtuple first and then tuple.
  if tree_utils.isinstance_of_namedtuple(obj):
    module_name, class_name = _module_and_class_name(obj.__class__)
    return dict(
        category='namedtuple',
        module=module_name,
        clazz=class_name,
        entries=[
            dict(key=k, value=_value_metadata_tree_for_json_dumps(v))
            for k, v in zip(obj._fields, obj)
        ],
    )
  # Check namedtuple first and then tuple.
  if isinstance(obj, tuple):
    return dict(
        category='custom',
        clazz='tuple',
        entries=[_value_metadata_tree_for_json_dumps(e) for e in obj],
    )

  if isinstance(obj, Mapping):
    return {k: _value_metadata_tree_for_json_dumps(v) for k, v in obj.items()}

  if isinstance(obj, list):
    return [_value_metadata_tree_for_json_dumps(e) for e in obj]

  # Handle objects that are registered as Jax container nodes.
  key_leafs, _ = jax.tree_util.tree_flatten_with_path(
      obj,
      is_leaf=lambda x: x is not obj,  # flatten just one level.
  )
  return {
      tree_utils.get_key_name(keypath[0]): _value_metadata_tree_for_json_dumps(
          leaf
      )
      for keypath, leaf in key_leafs
  }

