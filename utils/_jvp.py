
def _jvp(primals, tangents):
  (x, _), (_, t) = primals, tangents
  return x, t


def _jvp(fun: Callable, primals, tangents, has_aux=False):
  ps_ft = FlatTree.flatten(primals)
  ts_ft = FlatTree.flatten(tangents)
  if ps_ft.tree != ts_ft.tree:
    raise TypeError("primal and tangent arguments to jax.jvp must have the same tree "
                    f"structure; primals have tree structure {ps_ft.tree} whereas tangents have "
                    f"tree structure {ts_ft.tree}.")
  for p, t in zip(ps_ft, ts_ft):
    if not isinstance(core.typeof(p), ShapedArray): continue
    if core.primal_dtype_to_tangent_dtype(_dtype(p)) != _dtype(t):
      raise TypeError("primal and tangent arguments to jax.jvp do not match; "
                      "dtypes must be equal, or in case of int/bool primal dtype "
                      "the tangent dtype must be float0."
                      f"Got primal dtype {_dtype(p)} and so expected tangent dtype "
                      f"{core.primal_dtype_to_tangent_dtype(_dtype(p))}, but got "
                      f"tangent dtype {_dtype(t)} instead.")
    if np.shape(p) != np.shape(t):
      raise ValueError("jvp called with different primal and tangent shapes;"
                       f"Got primal shape {np.shape(p)} and tangent shape as {np.shape(t)}")

  out_primals, out_tangents, *aux = ad.jvp(fun, ps_ft, ts_ft, has_aux=has_aux)
  return out_primals.unflatten(), out_tangents.unflatten(), *aux

