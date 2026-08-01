
def linear_transpose2(transpose_rule, cotangent, *args, **kwargs):
  if type(cotangent) is Zero:
    return [Zero(x.aval.to_ct_aval()) if isinstance(x, UndefinedPrimal)
            else None for x in args]
  else:
    return transpose_rule(cotangent, *args, **kwargs)

