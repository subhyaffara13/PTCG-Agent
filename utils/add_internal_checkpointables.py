
def add_internal_checkpointables(
    checkpointables: dict[str, Any],
    *,
    context: context_lib.Context,
    metrics: tree_types.JsonType | None = None,
) -> dict[str, Any]:
  """Adds a descriptor to checkpointables if enabled.

  Args:
    checkpointables: A dictionary of checkpointables.
    context: The Orbax context.
    metrics: Optional metrics to add to the checkpointables.

  Returns:
    The updated dictionary of checkpointables.
  """
  # Global registration ties metrics key to JsonHandler.
  if metrics:
    checkpointables[checkpoint_layout.METRICS_CHECKPOINTABLE_KEY] = metrics
  return checkpointables

