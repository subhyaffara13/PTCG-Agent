
def _tangent_linear_map(func: Callable, params, params_dot,
                        debug_info: core.DebugInfo,
                        *x):
  """Compute the tangent of a linear map.

  Assuming ``func(*params, *x)`` is linear in ``x`` and computes ``A @ x``,
  this function computes ``∂A @ x``.
  """
  assert any(type(p) is not ad_util.Zero for p in params_dot)
  zeros = _map(ad_util.p2tz, x)
  primals_ft = FlatTree.flatten_list(params + list(x))
  tangents_ft = FlatTree.flatten_list(params_dot + zeros)
  _, out_tangent = ad.jvp(func, primals_ft, tangents_ft)
  return list(out_tangent)

