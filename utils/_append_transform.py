
def _append_transform(list_, transform):
  """Append `transform` to `list_` (with `ecolab` reload support)."""
  transform.__is_ecolab__ = True  # Marker to support `ecolab` adhoc `reload`
  list_.append(transform)

