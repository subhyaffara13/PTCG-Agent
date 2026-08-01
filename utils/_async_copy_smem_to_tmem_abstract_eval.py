
def _async_copy_smem_to_tmem_abstract_eval(
    smem_ref, tmem_ref, *args, smem_tree, tmem_tree, **_kwargs
):
  if smem_ref.memory_space != gpu_core.MemorySpace.SMEM:
    raise ValueError("async_copy_smem_to_tmem source must be an SMEM ref")
  if tmem_ref.memory_space != gpu_core.MemorySpace.TMEM:
    raise ValueError("async_copy_smem_to_tmem target must be a TMEM ref")
  smem_transforms, tmem_transforms = util.split_list(
      args, [smem_tree.num_leaves]
  )
  smem_aval = smem_ref
  for t in jax.tree.unflatten(smem_tree, smem_transforms):
    smem_aval = t.transform_type(smem_aval)
  tmem_aval = tmem_ref
  for t in jax.tree.unflatten(tmem_tree, tmem_transforms):
    tmem_aval = t.transform_type(tmem_aval)
  if smem_aval.dtype != tmem_aval.dtype:
    raise ValueError(
        f"Expected SMEM element type ({smem_aval.dtype}) to equal the TMEM"
        f" element type ({tmem_aval.dtype})"
    )
  if smem_aval.shape != tmem_aval.shape:
    raise ValueError(
        f"Expected SMEM reference shape {smem_aval.shape} to equal the TMEM"
        f" reference shape {tmem_aval.shape}"
    )
  return (), {state_types.ReadEffect(0), state_types.WriteEffect(1)}

