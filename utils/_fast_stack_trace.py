
def _fast_stack_trace():
  """A fast stack trace that gets us the minimal information we need.

  Compared to using `get_absl_logger().findCaller(stack_info=True)`, this
  function is ~100x faster.

  Returns:
    A tuple of tuples of (filename, line_number, last_instruction_offset).
  """
  cur_stack = inspect.currentframe()
  if cur_stack is None or cur_stack.f_back is None:
    return tuple()
  # We drop the first frame, which is this function itself.
  cur_stack = cur_stack.f_back
  call_stack = []
  while cur_stack.f_back:
    cur_stack = cur_stack.f_back
    call_stack.append(
        (cur_stack.f_code.co_filename, cur_stack.f_lineno, cur_stack.f_lasti)
    )
  return tuple(call_stack)

