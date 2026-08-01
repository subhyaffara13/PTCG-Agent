
def override_named_call(enable: bool = True):
  # pylint: disable=g-doc-return-or-yield
  """Returns a context manager that enables/disables named call wrapping.

  Args:
    enable: If true, enables named call wrapping for labelling profile traces.
      (see ``enabled_named_call``).
  """
  # pylint: enable=g-doc-return-or-yield
  global _use_named_call
  use_named_call_prev = _use_named_call
  _use_named_call = enable
  try:
    yield
  finally:
    _use_named_call = use_named_call_prev

