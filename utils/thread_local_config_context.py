
def thread_local_config_context(**kwds):
  stack = ExitStack()
  for config_name, value in kwds.items():
    stack.enter_context(config.config_states[config_name](value))
  try:
    yield
  finally:
    stack.close()

