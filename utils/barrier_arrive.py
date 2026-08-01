
def barrier_arrive(number_of_threads: _ods_ir.Value[_ods_ir.IntegerType], *, barrier_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BarrierArriveOp:
  return BarrierArriveOp(numberOfThreads=number_of_threads, barrierId=barrier_id, loc=loc, ip=ip)


def barrier_arrive(barrier: state.AbstractRef) -> None:
  """Arrives at the given barrier."""
  barrier, transforms = state_primitives.get_ref_and_transforms(
      barrier, None, "barrier_arrive"
  )
  flat_transforms, transforms_treedef = tree_util.tree_flatten(transforms)
  barrier_arrive_p.bind(
      barrier, *flat_transforms, transforms_treedef=transforms_treedef
  )

