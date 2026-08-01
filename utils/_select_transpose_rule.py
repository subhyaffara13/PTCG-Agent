
def _select_transpose_rule(ct, which, *cases):
  assert not ad.is_undefined_primal(which)
  if type(ct) is ad_util.Zero:
    return [None] + [ad_util.Zero(c.aval) if ad.is_undefined_primal(c) else None
                     for c in cases]
  else:
    zeros = full_like(ct, 0)
    if dtypes.dtype(which) == np.dtype(np.bool_):
      ct0 = select(which, zeros, ct) if ad.is_undefined_primal(cases[0]) else None
      ct1 = select(which, ct, zeros) if ad.is_undefined_primal(cases[1]) else None
      return (None, ct0, ct1)
    else:
      return [None] + [
          select(eq(which, _const(which, i)), ct, zeros)
          if ad.is_undefined_primal(case) else None for i, case in enumerate(cases)
      ]

