
def _value_metadata_tree_for_json_loads(obj):
  """Callback for `simplejson.loads` to convert JSON object to a PyTree."""
  if not isinstance(obj, Mapping):
    return obj

  if 'category' in obj:
    if obj['category'] == 'custom':
      if obj['clazz'] == _VALUE_METADATA_ENTRY_CLAZZ:
        return value_metadata_entry.ValueMetadataEntry.from_json(
            obj['data'],
            pytree_metadata_options_lib.PyTreeMetadataOptions(
                support_rich_types=True,  # Always in rich types mode.
            ),
        )
      if obj['clazz'] == 'tuple':
        return tuple(
            [(_value_metadata_tree_for_json_loads(v)) for v in obj['entries']]
        )
      raise ValueError(
          f'Unsupported "custom" object in JSON deserialization: {obj}'
      )

    if obj['category'] == 'namedtuple':
      return _create_namedtuple(
          module_name=obj['module'],
          class_name=obj['clazz'],
          attrs=[
              (
                  e['key'],
                  _value_metadata_tree_for_json_loads(e['value']),
              )
              for e in obj['entries']
          ],
      )

  return {k: _value_metadata_tree_for_json_loads(v) for k, v in obj.items()}

