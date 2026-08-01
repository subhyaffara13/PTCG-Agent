
def count_num_calls(fn):
  """Counts the number of times the function was called."""
  num_calls = 0

  @functools.wraps(fn)
  def fn_wrapped(*args, **kwargs):
    nonlocal num_calls
    num_calls += 1
    return fn(*args, **kwargs)

  return fn_wrapped, lambda: num_calls

