
def validate_state_checkpointable_name(
    checkpointable_name: str | None,
) -> None:
  """Validates the checkpointable name.

  Args:
    checkpointable_name: The name of the checkpointable.

  Raises:
    ValueError: If the checkpointable name is reserved.
  """
  if (
      checkpointable_name is None
      or checkpointable_name == checkpoint_layout.AUTO_CHECKPOINTABLE_KEY
  ):
    return
  if checkpointable_name == EMPTY_CHECKPOINTABLE_KEY:
    raise ValueError(
        'Empty string is not supported as a checkpointable name in'
        ' `load`. Checkpointable name must be a valid non-empty string'
        ' name or None if loading a legacy V0 direct pytree checkpoint.'
    )
  if checkpointable_name in RESERVED_CHECKPOINTABLE_KEYS:
    raise ValueError(
        f'Provided reserved checkpointable key: {checkpointable_name}.'
    )

