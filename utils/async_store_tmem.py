
def async_store_tmem(source: _ods_ir.Value[_ods_ir.VectorType], destination: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AsyncStoreTmemOp:
  return AsyncStoreTmemOp(source=source, destination=destination, loc=loc, ip=ip)


def async_store_tmem(ref: _Ref, value):
  """Stores the value to TMEM.

  The store is asynchronous and is not guaranteed to be visible (e.g. by reads
  or MMA operations) until ``commit_tmem`` has been called.

  Args:
    ref: The TMEM reference to store to.
    value: The value to store.
  """
  ref, ref_transforms = state_primitives.get_ref_and_transforms(
      ref, None, "async_store_tmem"
  )
  flat_ref_transforms, ref_transforms_treedef = tree_util.tree_flatten(
      ref_transforms
  )
  async_store_tmem_p.bind(
      ref, value, *flat_ref_transforms, tree=ref_transforms_treedef
  )

