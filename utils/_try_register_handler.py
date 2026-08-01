
def _try_register_handler(
    handler_type: type[handler_types.CheckpointableHandler],
    name: str | None = None,
    secondary_typestrs: Sequence[str] | None = None,
):
  """Tries to register handler globally with name and secondary typestrs."""
  try:
    registration.global_registry().add(
        handler_type,
        checkpointable_name=name,
        secondary_typestrs=secondary_typestrs,
    )
  except registration.AlreadyExistsError:
    pass

