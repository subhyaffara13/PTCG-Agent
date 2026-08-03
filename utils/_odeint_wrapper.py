from typing import Callable

def _odeint_wrapper(func: Callable, rtol, atol, mxstep, hmax, y0, ts, *args):
  y0, unravel = ravel_pytree(y0)
  debug = api_util.debug_info("odeint", func, args, {})
  func = ravel_first_arg(func, unravel, debug)
  out = _odeint(func, rtol, atol, mxstep, hmax, y0, ts, *args)
  return jax.vmap(unravel)(out)

