import os

def set_env(**kwargs):
  """Context manager to temporarily set/unset one or more environment variables.

  Caution: setting environment variables is not thread-safe. If you use this
  utility, you must annotate your test using, e.g., @thread_unsafe_test() or
  @thread_unsafe_test_class().

  Examples:

    >>> import os
    >>> os.environ['my_var'] = 'original'

    >>> with set_env(my_var=None, other_var='some_value'):
    ...   print("my_var is set:", 'my_var' in os.environ)
    ...   print("other_var =", os.environ['other_var'])
    ...
    my_var is set: False
    other_var = some_value

    >>> os.environ['my_var']
    'original'
    >>> 'other_var' in os.environ
    False
  """
  original = {key: os.environ.pop(key, None) for key in kwargs}
  os.environ.update({k: v for k, v in kwargs.items() if v is not None})
  try:
    yield
  finally:
    _ = [os.environ.pop(key, None) for key in kwargs]
    os.environ.update({k: v for k, v in original.items() if v is not None})

