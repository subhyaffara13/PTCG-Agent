
def validate_abstract_checkpointables(
    abstract_checkpointables: (
        dict[str, handler_types.AbstractCheckpointable] | None
    ),
) -> None:
  """Validates the abstract_checkpointables dictionary.

  Args:
    abstract_checkpointables: A dictionary of abstract checkpointables.

  Raises:
    ValueError: If any of the keys in abstract_checkpointables are reserved.
  """
  if abstract_checkpointables is None:
    return
  if not isinstance(abstract_checkpointables, dict):
    raise ValueError(
        '`abstract_checkpointables` must be a valid mapping of checkpointable'
        ' names to abstract checkpointables to load, but got'
        f' {type(abstract_checkpointables)}'
    )
  if EMPTY_CHECKPOINTABLE_KEY in abstract_checkpointables:
    raise ValueError(
        'Empty string is not supported as a checkpointable name in'
        ' `load_checkpointables`. Each checkpointable name must be a valid'
        ' non-empty string name.'
    )
  if (
      provided_reserved_keys := abstract_checkpointables.keys()
      & RESERVED_CHECKPOINTABLE_KEYS
  ):
    raise ValueError(
        f'Provided reserved checkpointable keys: {provided_reserved_keys}.'
    )

