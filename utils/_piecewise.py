from typing import Callable

def _piecewise(x: Array, condlist: Array, consts: dict[int, ArrayLike],
               funcs: frozenset[tuple[int, Callable[..., Array]]],
               *args, **kw) -> Array:
  funcdict = dict(funcs)
  funclist = [consts.get(i, funcdict.get(i)) for i in range(len(condlist) + 1)]
  indices = argmax(reductions.cumsum(concatenate(
      [array_creation.zeros_like(condlist[:1]), condlist], 0), 0), 0)
  dtype = x.dtype
  def _call(f):
    return lambda x: f(x, *args, **kw).astype(dtype)
  def _const(v):
    return lambda x: array(v, dtype=dtype)
  funclist = [_call(f) if callable(f) else _const(f) for f in funclist]
  return vectorize(control_flow.switch, excluded=(1,))(indices, funclist, x)

