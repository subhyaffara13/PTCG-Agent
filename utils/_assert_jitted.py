
def _assert_jitted(fn, fn_input, is_jitted):
  """Asserts that a function can be jitted or not.

  Args:
    fn: The function to be tested
    fn_input: Input to pass to the function
    is_jitted: Assert that the function can be jitted with jax.jit (True) or
    cannot be jitted (False), i.e. the fake jit is working correctly.
  """
  asserts.clear_trace_counter()
  max_traces = 1 if is_jitted else 0
  wrapped_fn = jax.jit(asserts.assert_max_traces(fn, max_traces))
  wrapped_fn(fn_input)

