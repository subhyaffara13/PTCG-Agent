
def async_copy_scales_to_tmem(
    smem_ref: _Ref, tmem_ref: _Ref, collective_axis: AxisName | None = None,
):
  """Copies the MMA scales from SMEM to TMEM.

  The copy is performed asynchronously and can be awaited by calling
  ``tcgen05_commit_arrive`` and waiting on the specified barrier. However, if
  the copy is consumed by an MMA operation issued in the same thread, no
  synchronization is necessary (except for eventually awaiting the MMA operation
  itself).
  """
  smem_ref, smem_transforms = state_primitives.get_ref_and_transforms(
      smem_ref, None, "async_copy_scales_to_tmem"
  )
  flat_smem_transforms, smem_transforms_treedef = tree_util.tree_flatten(
      smem_transforms
  )
  tmem_ref, tmem_transforms = state_primitives.get_ref_and_transforms(
      tmem_ref, None, "async_copy_scales_to_tmem"
  )
  flat_tmem_transforms, tmem_transforms_treedef = tree_util.tree_flatten(
      tmem_transforms
  )
  async_copy_scales_to_tmem_p.bind(
      smem_ref, tmem_ref, *flat_smem_transforms, *flat_tmem_transforms,
      smem_tree=smem_transforms_treedef, tmem_tree=tmem_transforms_treedef,
      collective_axis=collective_axis,
  )

