
def validate_save_checkpointables(
    checkpointables: dict[str, handler_types.Checkpointable],
) -> None:
  """Validates the checkpointables dictionary.

  Args:
    checkpointables: A dictionary of checkpointables.

  Raises:
    ValueError: If any of the keys in checkpointables are reserved.
  """
  if not checkpointables or not isinstance(
      checkpointables, dict
  ):
    raise ValueError(
        '`checkpointables` must be a valid dict of checkpointable names to'
        ' desired checkpointables to save, but got'
        f' {type(checkpointables)}'
    )

  if EMPTY_CHECKPOINTABLE_KEY in checkpointables:
    raise ValueError(
        'Empty string is not supported as a checkpointable name in'
        ' `save_checkpointables`. Each checkpointable name must be a valid'
        ' non-empty string name.'
    )
  if (
      provided_reserved_keys := checkpointables.keys()
      & RESERVED_CHECKPOINTABLE_KEYS
  ):
    raise ValueError(
        f'Provided reserved checkpointable keys: {provided_reserved_keys}.'
    )

