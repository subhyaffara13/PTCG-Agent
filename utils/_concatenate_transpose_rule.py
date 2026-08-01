
def _concatenate_transpose_rule(ct, *operands, dimension):
  operand_shapes = [o.aval.shape if ad.is_undefined_primal(o) else o.shape
                    for o in operands]
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(o.aval) if ad.is_undefined_primal(o) else None
            for o in operands]
  else:
    return split(ct, tuple(shape[dimension] for shape in operand_shapes),
                 axis=dimension)

