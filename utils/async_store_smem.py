
def async_store_smem(value_to_store: _ods_ir.Value[_ods_ir.VectorType], destination: _ods_ir.Value[_ods_ir.MemRefType], barrier: _ods_ir.Value[_ods_ir.MemRefType], cluster_dim: _Union[_Any, _ods_ir.Attribute], cluster_idx: _ods_ir.Value[_ods_ir.IntegerType], *, atomic_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, optimized: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AsyncStoreSmemOp:
  return AsyncStoreSmemOp(valueToStore=value_to_store, destination=destination, barrier=barrier, cluster_dim=cluster_dim, cluster_idx=cluster_idx, atomic_type=atomic_type, optimized=optimized, loc=loc, ip=ip)


def async_store_smem(
    src: jax.Array,
    ref: _Ref,
    barrier: _Ref,
    *,
    cluster_idx: jax.Array,
    cluster_dim: Hashable | int,
    optimized: bool = True,
    atomic: Literal["add", "max", "min", "and", "or", "xor"] | None = None,
) -> None:
  """Asynchronously stores an array to a SMEM reference within the cluster.

  Args:
    src: The array containing the data to be stored.
    ref: The SMEM reference to store to.
    barrier: The barrier to update when the copy has completed (in destination block).
    cluster_idx: The index of the target cluster block within cluster_dim.
    cluster_dim: The cluster axis of cluster_idx.
    optimized: If True, the store is guaranteed not to cause any bank conflicts.
    atomic: The reduction operation to apply instead of overwriting the data.
  """
  ref, ref_transforms = state_primitives.get_ref_and_transforms(
      ref, None, "async_store_smem"
  )
  barrier, barrier_transforms = state_primitives.get_ref_and_transforms(
      barrier, None, "async_store_smem"
  )
  flat_ref_transforms, ref_transforms_treedef = tree_util.tree_flatten(
      ref_transforms
  )
  flat_barrier_transforms, barrier_transforms_treedef = tree_util.tree_flatten(
      barrier_transforms
  )
  async_store_smem_p.bind(
      src,
      ref,
      barrier,
      cluster_idx,
      *flat_ref_transforms,
      *flat_barrier_transforms,
      ref_transforms_treedef=ref_transforms_treedef,
      barrier_transforms_treedef=barrier_transforms_treedef,
      cluster_dim=cluster_dim,
      optimized=optimized,
      atomic=atomic,
  )
  return None

