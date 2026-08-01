
def async_prefetch(source: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value], slice_lengths: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], collective: _Union[_Any, _ods_ir.ArrayAttr], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AsyncPrefetchOp:
  return AsyncPrefetchOp(source=source, indices=indices, slice_lengths=slice_lengths, collective=collective, predicate=predicate, loc=loc, ip=ip)


def async_prefetch(
    ref: _Ref,
    *,
    collective_axes: str | tuple[str, ...] | None = None,
    leader_tracked: CopyPartition | None = None,
) -> None:
  """Asynchronously prefetches a GMEM reference to the L2 cache.

  If collective_axes is specified, each CUDA block only prefetches a part of
  the ``ref``, with other parts covered by blocks that share the same index
  along the collective axis.

  Specifying leader_tracked and collective_axes doesn't change the semantics
  of the prefetch, but if it's followed by a GMEM to SMEM copy, then it allows
  us to reuse the same TMA descriptor.

  Args:
    ref: The source Ref. Must be in GMEM.
    collective_axes: The collective axes to use for the prefetch.
    leader_tracked: The partitioning to use for the prefetch.
  """
  ref, ref_transforms = state_primitives.get_ref_and_transforms(
      ref, None, "async_prefetch"
  )
  flat_ref_transforms, ref_transforms_treedef = tree_util.tree_flatten(
      ref_transforms
  )
  if isinstance(collective_axes, str):
    collective_axes = (collective_axes,)
  async_prefetch_p.bind(
      ref,
      *flat_ref_transforms,
      ref_transforms_treedef=ref_transforms_treedef,
      collective_axes=collective_axes,
      leader_tracked=leader_tracked,
  )
  return None

