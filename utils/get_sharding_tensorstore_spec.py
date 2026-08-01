
def get_sharding_tensorstore_spec(
    directory: str, param_name: str
) -> dict[str, Any]:
  kvstore_tspec = build_kvstore_tspec(
      directory, name='_sharding', use_ocdbt=False
  )
  param_name = base64.urlsafe_b64encode(param_name.encode()).decode('utf-8')
  return {
      'driver': 'json',
      'kvstore': kvstore_tspec,
      'json_pointer': f'/{param_name}',
  }

