
def _transpose_shape_rule(operand, *, permutation):
  if not isinstance(permutation, (tuple, list, np.ndarray)):
    msg = "transpose permutation must be a tuple/list/ndarray, got {}."
    raise TypeError(msg.format(type(permutation)))
  if tuple(sorted(permutation)) != tuple(range(operand.ndim)):
    msg = ("transpose permutation isn't a permutation of operand dimensions, "
           "got permutation {} for operand shape {}.")
    raise TypeError(msg.format(permutation, operand.shape))
  return tuple(operand.shape[old_idx] for old_idx in permutation)

