from typing import Callable

def _check_primal_refs(
    f: Callable, nondiff_argnums: Sequence[int], debug: core.DebugInfo, *args):
  _check_for_aliased_refs(f, nondiff_argnums, debug, args)
  out = f(*args)
  _check_for_returned_refs(f, out, 'primal', [], 0)
  return out

