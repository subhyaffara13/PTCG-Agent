
def convert_hlo(ctx: LoweringRuleContext, x, aval_in, aval_out):
  """Variant of convert that has HLO semantics.

  In particular, treat casts to boolean as x != 0, rather than truncating
  integer values (b/209440332)."""
  if (not dtypes.issubdtype(aval_out.dtype, dtypes.extended) and
      aval_out.dtype == np.dtype(np.bool_)):
    if dtypes.issubdtype(aval_in.dtype, np.inexact):
      compare_type = "FLOAT"
    elif dtypes.issubdtype(aval_in.dtype, np.signedinteger):
      compare_type = "SIGNED"
    else:
      compare_type = "UNSIGNED"
    x = compare_hlo(x, full_like_aval(ctx, 0, aval_in), "NE", compare_type)
    # continue, to adjust the shape if needed
  (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
  return hlo.convert(result_type, x)

