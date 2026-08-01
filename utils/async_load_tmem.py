
def async_load_tmem(source: _ods_ir.Value[_ods_ir.MemRefType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return AsyncLoadTmemOp(source=source, results=results, loc=loc, ip=ip).result


def async_load_tmem(src: _Ref, *, layout: SomeLayout | None = None) -> jax.Array:
  """Performs an asynchronous load from the TMEM array.

  The load operation is only partly asynchronous. The returned array can be used
  immediately, without any additional synchronization. However, it cannot be
  assumed that the read from TMEM has completed when the function returns. If
  you ever attempt to overwrite the read region, you should ensure that
  ``wait_load_tmem`` has been called before that happens. Failure to do so
  can result in nondeterministic data races.

  For example, the following sequence of operations at the end of the kernel is
  valid, even though the TMEM load is never awaited::

    smem_ref[...] = plgpu.async_load_tmem(tmem_ref)
    plgpu.commit_smem()
    plgpu.copy_smem_to_gmem(smem_ref, gmem_ref)
    plgpu.wait_smem_to_gmem(0)

  However, if the kernel was persistent and might reuse the TMEM again, the
  sequence should be extended with a call to ``wait_load_tmem``.

  Args:
    src: The TMEM reference to load from.
    layout: The optional layout hint to use for the resulting array.
  """
  src, src_transforms = state_primitives.get_ref_and_transforms(
      src, None, "async_load_tmem"
  )
  flat_src_transforms, src_transforms_treedef = tree_util.tree_flatten(
      src_transforms
  )
  result = async_load_tmem_p.bind(
      src, *flat_src_transforms, tree=src_transforms_treedef
  )
  if layout is not None:
    result = gpu_core.layout_cast(result, layout)
  return result

