from typing import Any, Union

def _lower_as_gpu_kernel(
    body,
    grid: tuple[int, int, int],
    cluster: tuple[int, int, int],
    block: tuple[int, int, int],
    in_shapes: tuple[Any, ...],
    out_shape,
    inout_shape,
    smem_scratch_shape: ShapeTree | Union[ShapeTree],
    lowering_semantics: LoweringSemantics,
    module_name: str,
    kernel_name: str,
    prof_spec: profiler.ProfilerSpec | None = None,
    jax_mesh: mesh_lib.Mesh | None = None,
    base_loc: ir.Location | None = None,
):
  ptr_ty = llvm.PointerType.get()
  token_ty = gpu.AsyncTokenType.get()
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)

  def _shape_to_ref_ty(shape: jax.ShapeDtypeStruct) -> ir.MemRefType:
    return ir.MemRefType.get(shape.shape, utils.dtype_to_ir_type(shape.dtype))

  in_ref_tys = [_shape_to_ref_ty(t) for t in in_shapes]
  inout_ref_tys = [_shape_to_ref_ty(t) for t in inout_shape]

  unwrap_output_tuple = False
  if isinstance(out_shape, list):
    out_shape = tuple(out_shape)
  elif not isinstance(out_shape, tuple):
    out_shape = (out_shape,)
    unwrap_output_tuple = not inout_shape
  out_ref_tys = [_shape_to_ref_ty(t) for t in out_shape]
  if prof_spec is not None:
    out_shape = (*out_shape, prof_spec.jax_buffer_type(grid, block))
    out_ref_tys.append(prof_spec.mlir_buffer_type(grid, block))

  module = ir.Module.create(loc=base_loc)
  dialect.register_dialect(module.context)
  attrs = module.operation.attributes
  attrs["sym_name"] = ir.StringAttr.get(module_name)
  arch_major, arch_minor = _infer_arch()
  attrs["mosaic_gpu.arch_major"] = ir.IntegerAttr.get(i32, arch_major)
  attrs["mosaic_gpu.arch_minor"] = ir.IntegerAttr.get(i32, arch_minor)

  # These are needed as nonlocal below.
  launch_ctx = None
  with ir.InsertionPoint(module.body):
    _declare_runtime_functions()
    global_scratch = llvm.GlobalOp(
        llvm.ArrayType.get(i8, 0),  # We don't know the shape yet.
        "global_scratch",
        ir.Attribute.parse("#llvm.linkage<external>"),
        addr_space=ir.IntegerAttr.get(i32, 4),  # GPU constant memory.
    )
    @func.FuncOp.from_py_func(ptr_ty, ptr_ty, name=f"{kernel_name}_mosaic_gpu")
    def main(token_ptr, buffers):
      nonlocal launch_ctx
      token = builtin.unrealized_conversion_cast([token_ty], [token_ptr])
      arg_refs = []
      # XLA will pass in inout refs again as outputs, but we ignore them.
      for i, ref_ty in enumerate([*in_ref_tys, *inout_ref_tys, *out_ref_tys]):
        ptr = llvm.load(ptr_ty, utils.getelementptr(buffers, [i], ptr_ty))
        arg_memref = utils.ptr_as_memref(ptr, ir.MemRefType(ref_ty))
        # Annotate so we can find the corresponding kernel argument during the
        # lowering.
        arg_memref.owner.attributes[launch_context.KERNEL_ARG_ID_ATTR] = (
            ir.IntegerAttr.get(i32, i)
        )
        arg_memref.owner.attributes[launch_context.ORIGINAL_KERNEL_ARG_ATTR] = (
            ir.UnitAttr.get()
        )
        arg_refs.append(arg_memref)

      collective_metadata = None
      num_peers = 0
      num_params = 0

      # Collective metadata parameter is used to lower collective operations
      # in a single-process setup or in multi-process when nvshmem is not
      # available.
      if (
          jax_mesh is not None
          and jax_mesh.size > 1
          and (
              is_single_process_multi_device_topology()
              or not is_nvshmem_available()
          )
      ):
        num_params = len(arg_refs) + len(inout_ref_tys)
        num_peers = jax_mesh.size
        metadata_ptr = llvm.load(
            ptr_ty, utils.getelementptr(buffers, [num_params], ptr_ty)
        )

        metadata_ty = ir.MemRefType.get(
            (launch_context.get_collective_metadata_size(num_params, num_peers),),
            ir.IntegerType.get_signless(64),
        )
        collective_metadata = utils.ptr_as_memref(metadata_ptr, metadata_ty)

      prof_buffer = arg_refs.pop() if prof_spec is not None else None

      with _launch(
          token,
          grid,
          cluster,
          block,
          smem_scratch_shape,
          lowering_semantics,
          module,
          buffers,
          prof_spec,
          prof_buffer,
          collective_metadata,
          num_peers,
          num_params,
      ) as (_launch_ctx, smem_refs):
        launch_ctx = _launch_ctx
        body(launch_ctx, *arg_refs, smem_refs)
    main.func_op.attributes["llvm.emit_c_interface"] = ir.UnitAttr.get()
  sym_tab = ir.SymbolTable(module.operation)
  sym_tab.insert(main.func_op)
  sym_tab.insert(global_scratch)
  module.operation.verify()

  assert launch_ctx is not None
  return module, out_shape, unwrap_output_tuple, launch_ctx

