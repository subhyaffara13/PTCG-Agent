
def _lowering_context(
    module: ir.Module,
    launch_context: lc.LaunchContext | None,
    auto_barriers: bool,
) -> LoweringContext:
  """Returns a `LoweringContext` for the given `LaunchContext`."""
  # TODO(bchetioui): fix tests to not have a test-only path polluting the API.
  if launch_context is None:  # this case is used in some tests
    return LoweringContext(None, None, None, None, None, auto_barriers, 10**9)

  gpu_launch_op = _gpu_launch_op(module)
  with ir.InsertionPoint.at_block_begin(gpu_launch_op.regions[0].blocks[0]):
    eq = arith.CmpIPredicate.eq
    i32 = ir.IntegerType.get_signless(32)
    single_warp_per_block_predicate = arith.cmpi(
        eq, utils.warp_idx(sync=False), utils.c(0, i32)
    )
    smem_size = gpu_launch_op.dynamicSharedMemorySize
    assert smem_size is not None
    assert isinstance(smem_size.owner, arith.ConstantOp)
    smem_size = ir.IntegerAttr(smem_size.owner.value).value
    return LoweringContext(
        launch_context,
        utils.single_thread_predicate(scope=utils.ThreadSubset.WARP),
        utils.single_thread_predicate(scope=utils.ThreadSubset.WARPGROUP),
        utils.single_thread_predicate(scope=utils.ThreadSubset.BLOCK),
        single_warp_per_block_predicate,
        auto_barriers,
        smem_size,
    )

