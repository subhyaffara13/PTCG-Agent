
def locate_closest_backend(
    backends: Sequence[db_schema.StorageBackend],
    zone: str | None,
    region: str | None,
) -> db_schema.StorageBackend | None:
  """Selects the closest storage backend matching input location metrics.

  Attempts to match the client's zone or region with the available backends.
  If zone is provided, it tries to match the exact zone, or falls back to
  matching the zone prefix with backend region/multi-regions if no region is
  specified. If region is provided, it tries to match the region.

  Args:
    backends: A sequence of StorageBackend objects to choose from.
    zone: The client's zone, or None.
    region: The client's region, or None.

  Returns:
    The closest matching StorageBackend, or None if no match is found.
  """
  if zone is not None:
    # Match the exact zone.
    for backend in backends:
      if backend.zone == zone:
        return backend

    # When no region specified, match the zone prefix with the region.
    if region is None:
      for backend in backends:
        if backend.region is not None and zone.startswith(backend.region):
          return backend
        if backend.multi_regions is not None and zone.startswith(
            tuple(backend.multi_regions)
        ):
          return backend

  if region is not None:
    for backend in backends:
      if backend.region == region:
        return backend
      if backend.multi_regions is not None and region in backend.multi_regions:
        return backend

  return None

