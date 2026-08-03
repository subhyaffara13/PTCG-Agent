from typing import Any

def _lower_and_eval(
    name: str, jaxpr: core.ClosedJaxpr, args: Sequence[Any]
) -> list[Any]:
  from jax._src.lax.eval_jaxpr import eval_jaxpr_p  # pyrefly: ignore[missing-import]
  if any(aval.has_qdd for aval in jaxpr.in_aval_qdds):
    raise NotImplementedError(f"{name!r} does not support qdd on inputs")
  if any(aval.has_qdd for aval in jaxpr.final_aval_qdds):
    raise NotImplementedError(f"{name!r} does not support qdd on outputs")

  lo_jaxpr = pe.lower_jaxpr2(jaxpr)
  lo_args = [
      lo_val for aval, x in zip(jaxpr.in_avals, args)
      for lo_val in aval.lower_val(x)  # pyrefly: ignore[missing-attribute]
  ]
  lo_outs = eval_jaxpr_p.bind(*lo_args, jaxpr=lo_jaxpr)
  lo_outs_ = iter(lo_outs)
  hi_outs = [
      t.raise_val(*it.islice(lo_outs_, len(t.lo_ty())))
      for t in jaxpr.out_avals
  ]
  assert next(lo_outs_, None) is None
  return hi_outs

