
def io_callback_jvp_rule(*args, **kwargs):
  del args, kwargs
  raise ValueError("IO callbacks do not support JVP.")

