
def assert_global_configs_unchanged():
  starting_cache = compilation_cache._cache
  starting_config = config.config.values.copy()
  yield
  ending_config = config.config.values
  ending_cache = compilation_cache._cache

  if starting_config != ending_config:
    differing = {k: (starting_config.get(k, NotPresent()), ending_config.get(k, NotPresent()))
                  for k in (starting_config.keys() | ending_config.keys())
                  if (k not in starting_config or k not in ending_config
                      or starting_config[k] != ending_config[k])}
    raise AssertionError(f"Test changed global config values. Differing values are: {differing}")
  if starting_cache is not ending_cache:
    raise AssertionError(
        f"Test changed the compilation cache object: before test it was "
        f"{starting_cache}, now it is {ending_cache}"
    )

