
def setup_shared_value_context() -> contextlib.AbstractContextManager[None]:
  """Returns a context manager for the shared value context.

  Within this context manager, `_shared_object_ids_seen` will refer
  to a consistent tracker. This tracker can then be used to check for repeated
  appearances of the same mutable object.

  This should be included in the `context_builders` argument to any renderer
  that checks for shared values.
  """
  return _shared_object_ids_seen.set_scoped(_SharedObjectTracker({}, set()))

