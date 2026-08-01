
def _construct_smem_reftree(
    cluster_shape: tuple[int, int, int],
    dynamic_smem: ir.Value,
    smem_buffers: ShapeTree,
    tmem_allocs: list[
        _TMEMAlloc | _TMEMDialectAlloc
    ],  # Mutated by this function!
    lowering_semantics: LoweringSemantics,
    dynamic_smem_offset: int = 0,
) -> Callable[[], RefTree]:
  i32 = ir.IntegerType.get_signless(32)
  i64 = ir.IntegerType.get_signless(64)
  flat_ref_tys, smem_buffer_tree = jax.tree.flatten(
      smem_buffers, is_leaf=lambda x: isinstance(x, Union)
  )
  smem_refs = []

  for ref_ty in flat_ref_tys:
    def barrier_memref(num_barriers: int) -> ir.Value:
      nonlocal dynamic_smem_offset
      barrier_ty = ir.MemRefType.get(
          (num_barriers,),
          dialect.BarrierType.get()
          if lowering_semantics == LoweringSemantics.Warpgroup
          else i64,
          memory_space=utils.smem(),
      )
      barrier_memref = _slice_smem(
            barrier_ty,
            dynamic_smem,
            dynamic_smem_offset,
            lowering_semantics,
        )
      dynamic_smem_offset += num_barriers * utils.MBARRIER_BYTES
      return barrier_memref
    ref: Any
    match ref_ty:
      case Union(members):
        member_thunks = [
            _construct_smem_reftree(
                cluster_shape,
                dynamic_smem,
                m,
                tmem_allocs,
                lowering_semantics,
                dynamic_smem_offset,
            )
            for m in members
        ]
        # TODO(apaszke): This is quadratic, but it shouldn't matter for now...
        dynamic_smem_offset += _smem_tree_size(ref_ty)

        def ref(member_thunks=member_thunks):
          return Union([t() for t in member_thunks])

      case TMABarrier(num_barriers):
        init_fn: Callable[..., Any] = (
            functools.partial(
                utils.DialectBarrierRef.initialize,
                orders_tensor_core=False,
            )
            if lowering_semantics == LoweringSemantics.Warpgroup
            else utils.BarrierRef.initialize
        )
        ref = init_fn(barrier_memref(num_barriers), arrival_count=1)
      case Barrier(arrival_count, num_barriers, orders_tensor_core):
        init_fn = (
            functools.partial(
                utils.DialectBarrierRef.initialize,
                orders_tensor_core=orders_tensor_core,
            )
            if lowering_semantics == LoweringSemantics.Warpgroup
            else utils.BarrierRef.initialize
        )
        ref = init_fn(barrier_memref(num_barriers), arrival_count=arrival_count)
      case ClusterBarrier(collective_dims, arrival_count, num_barriers):
        ref = utils.CollectiveBarrierRef.initialize(
            barrier_memref(num_barriers), arrival_count, collective_dims,
            cluster_shape, leader_tracked=ref_ty.leader_tracked
        )
      case TMEM(shape, dtype, layout=layout, collective=collective, packing=packing):
        addr_ref = _slice_smem(
            ir.MemRefType.get([], i32, memory_space=utils.smem()),
            dynamic_smem,
            dynamic_smem_offset,
            lowering_semantics,
        )
        packing = 1 if packing is None else packing
        ir_dtype = utils.dtype_to_ir_type(dtype)
        if lowering_semantics == LoweringSemantics.Warpgroup:
          if layout is not None:
            packing = layout.vector_length

          alloc = _TMEMDialectAlloc(
              addr_ref, shape, ir_dtype, packing, collective
          )
          tmem_allocs.append(alloc)
          def ref(alloc=alloc, layout=layout):
            assert alloc.tmem_ref is not None
            if layout is not None:
              layout_attr = layouts.to_layout_attr(layout)
              return dialect.tmem_layout_cast(alloc.tmem_ref, layout_attr)
            else:
              return alloc.tmem_ref

        else:
          if layout is None:
            layout = tcgen05._infer_tmem_layout(shape, collective, packing)
          num_cols = layout.cols_in_shape(shape, utils.bitwidth(ir_dtype))
          tmem_allocs.append(_TMEMAlloc(addr_ref, num_cols, collective))
          def ref(addr_ref=addr_ref, shape=shape, ir_dtype=ir_dtype, layout=layout):
            addr = memref.load(addr_ref, [])
            return tcgen05.TMEMRef(addr, shape, ir_dtype, layout)

        dynamic_smem_offset += 4  # i32 takes up 4 bytes
      case _:
        mlir_dtype = utils.dtype_to_ir_type(ref_ty.dtype)
        tile_smem = _slice_smem(
            ir.MemRefType.get(ref_ty.shape, mlir_dtype, memory_space=utils.smem()),
            dynamic_smem,
            dynamic_smem_offset,
            lowering_semantics,
        )
        dynamic_smem_offset += _count_buffer_bytes(ref_ty)
        ref = tile_smem
    smem_refs.append(ref)
  def ref_tree_thunk():
    refs = []
    for ref in smem_refs:
      if callable(ref):
        ref = ref()
      refs.append(ref)
    return jax.tree.unflatten(smem_buffer_tree, refs)
  return ref_tree_thunk

