
def _compare_lower_hlo_opaque(direction: str, ctx, avals_in, aval_out, x, y):
  broadcast_avals_in = tuple(
      core.ShapedArray(aval_out.shape, aval.dtype) for aval in avals_in)
  if direction == 'EQ':
    return _opaque_eq_hlo(ctx, broadcast_avals_in, aval_out, x, y)
  elif direction == 'NE':
    return _opaque_ne_hlo(ctx, broadcast_avals_in, aval_out, x, y)
  else:
    raise NotImplementedError(
        f"HLO comparison {direction} for extended dtype {avals_in[0].dtype}")

