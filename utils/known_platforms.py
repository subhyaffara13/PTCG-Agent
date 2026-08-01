
def known_platforms() -> set[str]:
  platforms = set()
  platforms |= set(_nonexperimental_plugins)
  platforms |= set(_backend_factories.keys())
  platforms |= set(_platform_aliases.values())
  platforms |= set(_platform_aliases.keys())
  return platforms

