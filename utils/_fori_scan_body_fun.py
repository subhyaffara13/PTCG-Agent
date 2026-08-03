from typing import Callable

def _fori_scan_body_fun(body_fun: Callable, body_fun_dbg: core.DebugInfo) -> Callable:
  body_fun_ref = weakref.ref(body_fun)
  def scanned_fun(loop_carry, _):
    i, x = loop_carry
    body_fun = body_fun_ref()
    assert body_fun is not None
    return (i + 1, body_fun(i, x)), None
  api_util.save_wrapped_fun_debug_info(
      scanned_fun, body_fun_dbg._replace(result_paths=None))
  return scanned_fun

