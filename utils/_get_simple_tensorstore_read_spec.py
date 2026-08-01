
def _get_simple_tensorstore_read_spec(
    checkpoint_directory: epath.Path,
    param_name: str,
    use_zarr3: bool,
    use_ocdbt: bool,
) -> Dict[str, Any]:
  """Returns a simple TensorStore read spec for testing."""
  if use_ocdbt:
    ts_spec = {
        'driver': 'zarr3' if use_zarr3 else 'zarr',
        'kvstore': {
            'driver': 'ocdbt',
            'base': f'file://{checkpoint_directory}',
            'path': param_name,
        },
    }
  else:
    ts_spec = {
        'driver': 'zarr3' if use_zarr3 else 'zarr',
        'kvstore': {
            'driver': 'file',
            'path': f'{checkpoint_directory/ param_name}',
        },
    }

  return ts_spec

