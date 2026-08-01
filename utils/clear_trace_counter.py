
def clear_trace_counter() -> None:
  """Clears Chex traces' counter for ``assert_max_traces`` checks.

  Use it to isolate unit tests that rely on ``assert_max_traces``,
  by calling it at the start of the test case.
  """
  _ai.TRACE_COUNTER.clear()

