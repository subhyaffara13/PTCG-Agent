
def _permutation_to_affine_map_attr(
    permutation: Sequence[int],
) -> ir.AffineMapAttr:
  return ir.AffineMapAttr.get(ir.AffineMap.get_permutation(permutation))

