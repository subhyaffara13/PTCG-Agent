
def check_impl(*args, err_tree, debug):
  if debug:
    # NOOP (check will only trigger when discharged)
    return []
  error = tree_unflatten(err_tree, args)
  exc = error.get_exception()
  if exc:
    filtered_tb = traceback_util.filter_traceback(
        exc.traceback_info.as_python_traceback())
    exc.with_traceback(filtered_tb)
    raise JaxRuntimeError(str(exc)) from exc
  return []

