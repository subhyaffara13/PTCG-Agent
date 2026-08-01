
def is_known_platform(platform: str) -> bool:
  # A platform is valid if there is a registered factory for it. It does not
  # matter if we were unable to initialize that platform; we only care that
  # we've heard of it and it isn't, e.g., a typo.
  return platform in known_platforms()

