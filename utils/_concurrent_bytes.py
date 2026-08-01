
def _concurrent_bytes(
    concurrent_gb: int | str | None, *, use_default_if_none: bool = True
) -> int | str | None:
  if concurrent_gb == 'auto':
    return 'auto'
  if concurrent_gb is None:
    if use_default_if_none:
      return DEFAULT_CONCURRENT_GB * 10**9
    else:
      return None
  else:
    return concurrent_gb * 10**9

