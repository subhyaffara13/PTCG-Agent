
def is_compression_used(
    checkpoint_directory: epath.Path,
    param_name: str,
    use_zarr3: bool,
    use_ocdbt: bool,
):
  """Returns True if compression is used for a given paramin in Tensorstore."""
  ts_spec = _get_simple_tensorstore_read_spec(
      checkpoint_directory, param_name, use_zarr3, use_ocdbt
  )
  read_spec = ts.open(ts_spec).result().spec().to_json()

  if use_zarr3:
    # check if zstd is in the codecs
    for codec in read_spec['metadata']['codecs'][0]['configuration']['codecs']:
      if codec['name'] == 'zstd':
        return True
    return False

  else:
    return read_spec['metadata']['compressor'] is not None

