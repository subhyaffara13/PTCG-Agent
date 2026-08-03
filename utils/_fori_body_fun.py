from typing import Callable

def _fori_body_fun(body_fun: Callable, body_fun_dbg: core.DebugInfo) -> Callable:
  body_fun_ref = weakref.ref(body_fun)

  def while_body_fun(loop_carry):
    i, upper, x = loop_carry
    body_fun = body_fun_ref()
    assert body_fun is not None
    return lax.add(i, lax._const(i, 1)), upper, body_fun(i, x)
  if body_fun_dbg.arg_names is not None:
    arg_names = (body_fun_dbg.arg_names[0],
                 "",  # upper,
                 * body_fun_dbg.arg_names[1:])
  else:
    arg_names = None
  api_util.save_wrapped_fun_debug_info(
      while_body_fun,
      body_fun_dbg._replace(arg_names=arg_names))
  return while_body_fun

