
def io_callback_transpose_rule(*args, **kwargs):
  del args, kwargs
  raise ValueError("IO callbacks do not support transpose.")

