
def standard_vma_rule(prim_name, *avals, **kwargs) -> frozenset[AxisName]:
  if not config._check_vma.value:
    return frozenset()
  avals = tuple(a for a in avals if a is not abstract_token)
  if not avals:
    return frozenset()
  vma, *vmas = (a.mat.varying for a in avals)
  if not all(vma == vma_ for vma_ in vmas):
    raise ValueError(
        f'Primitive {prim_name} requires varying manual axes '
        f'to match, but got {[vma, *vmas]}. Please open an issue at '
        'https://github.com/jax-ml/jax/issues and as a temporary '
        'workaround pass the check_vma=False argument to `jax.shard_map`')
  return vma

