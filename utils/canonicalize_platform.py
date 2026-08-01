
def canonicalize_platform(platform: str) -> str:
  """Replaces platform aliases with their concrete equivalent.

  In particular, replaces "gpu" with either "cuda", "oneapi" or "rocm", depending on which
  hardware is actually present. We want to distinguish "cuda", "oneapi" and "rocm" for
  purposes such as MLIR lowering rules, but in many cases we don't want to
  force users to care.
  """
  platforms = _alias_to_platforms.get(platform, None)
  if platforms is None:
    return platform

  b = backends()
  for p in platforms:
    if p in b.keys():
      return p
  raise RuntimeError(f"Unknown backend: '{platform}' requested, but no "
                     f"platforms that are instances of {platform} are present. "
                     "Platforms present are: " + ",".join(b.keys()))

