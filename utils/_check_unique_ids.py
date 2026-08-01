
def _check_unique_ids(name: str, ids: tuple[int, ...]) -> None:
  """Checks that all integer IDs in the given tuple are unique."""
  duplicates = {
      id_ for id_, count in collections.Counter(ids).items() if count > 1
  }
  if duplicates:
    raise ValueError(
        f'{name} must be unique. Duplicate ids: {sorted(duplicates)}.'
    )

