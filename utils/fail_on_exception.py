
def fail_on_exception(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    shared_memory = _get_shared_memory()

    try:
      # TODO(jburnim): Pass `shared_memory` to `func`, so it does not have to
      # call `_get_shared_memory` again?
      shared_memory.check_failed()
      return func(*args, **kwargs)
    except Exception as e:
      # NOTE: If args is long enough, for the decorated function:
      #   - `token` is always args[0]
      #   - `device_id` is always args[1]
      #   - `local_core_id` is always args[2]
      token = int(args[0])
      device_id = None
      local_core_id = None
      if len(args) > 1:
        try:
          device_id = int(args[1])
        except:
          pass
      if len(args) > 2:
        try:
          local_core_id = int(args[2])
        except:
          pass
      shared_memory.set_failed(
          e, device_id=device_id, local_core_id=local_core_id,
          # NOTE: To avoid having to pass around a separate value to track
          # whether or not this callback is running at the "top level" (vs.
          # inside of a thread_map), we set the token to a specific value for
          # the top-level interpret_pallas_call/_interpret_jaxpr calls vs.
          # those inside thread_map.
          top_level=(token == TOP_LEVEL_TOKEN_VALUE))
      raise

  return wrapper

