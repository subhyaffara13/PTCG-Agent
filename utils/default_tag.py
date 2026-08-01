
def default_tag(event: str) -> str:
  """Tag for an in-prefix event we don't have an explicit mapping for.

  Routes into 9_other/ so unmapped events stay visible (queryable in the
  dashboard) without polluting the curated 2_/3_/4_/5_ namespaces. The
  leading "/jax/" is redundant (every captured event has it) so it's stripped.

  Args:
    event: The raw jax.monitoring event name (e.g. `/jax/.../duration`).

  Returns:
    The `9_other/`-prefixed dashboard tag for the event.
  """
  stripped = event.removeprefix("/jax/").lstrip("/")
  return "9_other/" + stripped.replace("/", "_")

