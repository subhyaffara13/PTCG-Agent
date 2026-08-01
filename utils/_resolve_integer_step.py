
def _resolve_integer_step(
    step: int | CheckpointMetadata,
) -> int:
  if isinstance(step, int):
    return step
  return step.step

