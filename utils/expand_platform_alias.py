
def expand_platform_alias(platform: str) -> list[str]:
  """Expands, e.g., "gpu" to ["cuda", "rocm", "oneapi"].

  This is used for convenience reasons: we expect cuda and rocm to act similarly
  in many respects since they share most of the same code.
  """
  return _alias_to_platforms.get(platform, [platform])

