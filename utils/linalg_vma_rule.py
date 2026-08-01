
def linalg_vma_rule(multiple_results, shape_rule, name, *avals, **kwargs):
  output_shapes = shape_rule(*avals, **kwargs)
  out_vma = core.standard_vma_rule(name, *avals)
  if multiple_results:
    return [out_vma] * len(output_shapes)
  else:
    return out_vma

