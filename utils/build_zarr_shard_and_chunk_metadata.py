
def build_zarr_shard_and_chunk_metadata(
    *,
    global_shape: Shape,
    shard_shape: Shape,
    use_compression: bool = True,
    use_zarr3: bool,
    chunk_shape: Shape,
) -> JsonSpec:
  """Constructs Zarr metadata for TensorStore array write spec."""
  metadata = {'shape': global_shape}

  if not use_zarr3:
    # Zarr v2.
    metadata['chunks'] = chunk_shape
    if use_compression:
      metadata['compressor'] = {'id': 'zstd'}
    else:
      metadata['compressor'] = None
  else:
    # Zarr v3.
    metadata['chunk_grid'] = {
        'name': 'regular',
        'configuration': {
            'chunk_shape': chunk_shape,
        },
    }
    # TODO: b/354139177 - Consider if using write shape equal to shard shape and
    # read shape equal to chosen chunk shape would be a better setting.
    del shard_shape  # Currently unused.
    metadata['codecs'] = [
        {
            'name': 'sharding_indexed',
            'configuration': {
                'chunk_shape': chunk_shape,
                'codecs': [
                    {'name': 'bytes', 'configuration': {'endian': 'little'}},
                ],
                'index_codecs': [
                    {'name': 'bytes', 'configuration': {'endian': 'little'}},
                    {'name': 'crc32c'},
                ],
                'index_location': 'end',
            },
        },
    ]
    if use_compression:
      # Remove zstd codec if not using compression.
      metadata['codecs'][0]['configuration']['codecs'].append({'name': 'zstd'})

  return metadata

