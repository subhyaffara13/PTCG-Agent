import itertools

def _get_next_log_count_per_token(token):
  """Wrapper for _log_counter_per_token. Thread-safe.

  Args:
    token: The token for which to look up the count.

  Returns:
    The number of times this function has been called with
    *token* as an argument (starting at 0).
  """
  # Can't use a defaultdict because defaultdict isn't atomic, whereas
  # setdefault is.
  return next(_log_counter_per_token.setdefault(token, itertools.count()))

