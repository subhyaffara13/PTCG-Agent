
def _get_backend_key(
    level: int,
    zone: str | None,
    region: str | None,
    multi_regions: list[str] | None,
) -> tuple[int, str | None, str | None, tuple[str, ...] | None]:
  """Generates a unique key for a StorageBackend based on level and location."""
  return (
      level,
      zone,
      region,
      tuple(sorted(multi_regions)) if multi_regions else None,
  )

