
def _remap_sharding_metadata(metadata: dict[str, tp.Any]) -> None:
  if 'sharding' in metadata:
    warnings.warn(
      "'sharding' is deprecated, use 'out_sharding' instead.",
      DeprecationWarning,
      stacklevel=3,
    )
    metadata['out_sharding'] = metadata.pop('sharding')
  if 'sharding_names' in metadata:
    warnings.warn(
      "'sharding_names' is deprecated, use 'out_sharding' instead.",
      DeprecationWarning,
      stacklevel=3,
    )
    metadata['out_sharding'] = metadata.pop('sharding_names')

