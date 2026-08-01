
def add_flag_prefixes(flag_prefixes: list[str]) -> None:
  """Add flag prefixes to include in the cache key. Call prior to get().
  """
  global _extra_flag_prefixes
  _extra_flag_prefixes += flag_prefixes

