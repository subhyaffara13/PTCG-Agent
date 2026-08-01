
def global_config_context(**kwds):
  original_config = {}
  try:
    for key, value in kwds.items():
      original_config[key] = config._read(key)
      config.update(key, value)
    yield
  finally:
    for key, value in original_config.items():
      config.update(key, value)

