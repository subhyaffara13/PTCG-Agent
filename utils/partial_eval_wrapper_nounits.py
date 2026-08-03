from typing import Any, Callable

def partial_eval_wrapper_nounits(
    f: Callable,
    store: lu.Store,
    in_knowns: Sequence[bool],
    in_avals: Sequence[AbstractValue],
    *in_consts: Any):
  in_avals_, in_consts_ = iter(in_avals), iter(in_consts)
  in_pvals = [PartialVal.known(next(in_consts_)) if known else
              PartialVal.unknown(next(in_avals_)) for known in in_knowns]
  sentinel = object()
  assert next(in_avals_, sentinel) is next(in_consts_, sentinel) is sentinel
  jaxpr, (*maybe_fwds, out_pvals, res, env) = f(in_pvals)
  out_knowns, out_avals, out_consts = partition_pvals(out_pvals)
  store.store((*maybe_fwds, out_knowns, out_avals, jaxpr, env))
  return (*out_consts, *res)

