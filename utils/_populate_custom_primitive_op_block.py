
def _populate_custom_primitive_op_block(
    ctx: lowering.LoweringRuleContext,
    block: ir.Block,
    mgpu_fn: Callable[..., Any],
    pytree_args,
    in_layouts: Sequence[ir.Attribute],
    in_transforms: Sequence[ir.ArrayAttr],
    results_ty: Sequence[ir.Type],
    out_layouts: Sequence[ir.Attribute | None],
):
  """Calls the given mgpu_fn to populate the block, handling inputs and outputs.

  Block arguments that are references to SMEM or vectors are unwrapped to
  transformed references and fragmented arrays before they are passed to the
  python function mgpu_fn.

  The resulting fragmented arrays, if any, are wrapped as vectors before they
  are returned.
  """
  with ir.InsertionPoint(block):
    fn_inputs: list[ir.Value | mgpu.FragmentedArray] = []
    in_layouts_it = iter(in_layouts)
    in_transforms_it = iter(in_transforms)
    avals_in = ctx.avals_in[:pytree_args.num_leaves]
    for arg, aval in zip(block.arguments, avals_in, strict=True):
      if isinstance(arg.type, ir.MemRefType):
        memref_ty = ir.MemRefType(arg.type)
        if not mgpu_utils.is_smem_ref(memref_ty):
          fn_inputs.append(arg)
          continue

        transforms = ir.ArrayAttr(next(in_transforms_it))
        # The block arguments in the Mosaic GPU dialect are logical refs that
        # wrap the transfromed refs. Since the mgpu_fn works at the lowered
        # "lane" level, we need to transform (lower) the inputs before passing
        # them to the mgpu_fn.
        transformed_type = mgpu.dialect_lowering.transform_type(
            memref_ty, transforms
        )
        conversion_cast = builtin_dialect.UnrealizedConversionCastOp(
            [transformed_type], [arg]
        )
        fn_inputs.append(conversion_cast.result)
      elif isinstance(arg.type, ir.VectorType):
        layout_attr = next(in_layouts_it)
        layout = mgpu.layouts.from_layout_attr(layout_attr)

        vector_ty = ir.VectorType(arg.type)
        reg_shape = layout.registers_shape(tuple(vector_ty.shape))
        reg_ty = layout.registers_element_type(vector_ty.element_type)

        # The vector block arguments in the Mosaic GPU dialect are wrapped
        # Fragmented Arrays. Since the mgpu_fn works at the lowered
        # "lane" level, we need to unwrap (lower) the input vectors before
        # passing them to the mgpu_fn.
        conversion_cast = builtin_dialect.UnrealizedConversionCastOp(
            [reg_ty] * math.prod(reg_shape), [arg]
        )
        conversion_cast.attributes["registers_shape"] = ir.ArrayAttr.get([
            ir.IntegerAttr.get(ir.IntegerType.get_signless(64), s)
            for s in reg_shape
        ])
        conversion_cast.attributes["layout"] = layout_attr

        registers = np.array(list(conversion_cast.results)).reshape(reg_shape)
        is_signed = mgpu_utils.is_signed(aval.dtype)
        fa = mgpu.FragmentedArray(
            _registers=registers, _layout=layout, _is_signed=is_signed
        )
        fn_inputs.append(fa)
      else:  # scalar case.
        is_signed = mgpu_utils.is_signed(aval.dtype)
        fa = mgpu.FragmentedArray.splat(arg, (), is_signed=is_signed)
        fn_inputs.append(fa)

    args = jax.tree.unflatten(pytree_args, fn_inputs)
    inner_ret = mgpu_fn(ctx.launch_ctx, *args)
    if inner_ret is None:
      inner_ret = []
    elif not isinstance(inner_ret, tuple) and not isinstance(inner_ret, list):
      inner_ret = [inner_ret]
    ir_ret = []
    for fa, result_ty, out_layout in zip(
        inner_ret, results_ty, out_layouts, strict=True
    ):
      if not isinstance(fa, mgpu.FragmentedArray):
        raise ValueError(f"Expected a FragmentedArray, but got: {fa}")
      if isinstance(result_ty, ir.VectorType):
        result_shape = ir.VectorType(result_ty).shape
        if fa.shape != tuple(result_shape):
          raise ValueError(f"Expected {result_shape} but got {fa.shape}")
        if out_layout != mgpu.layouts.to_layout_attr(fa.layout):
          raise ValueError(
              f"Output layout {out_layout} does not match the layout of the"
              f" returned fragmented array {fa.layout}."
          )
        ir_ret.append(
            mgpu.dialect_lowering.fragmented_array_to_ir(fa, result_ty)
        )
      else:  # scalar case.
        assert out_layout is None
        if fa.shape:
          raise ValueError(f"Expected 0D shape, but got {fa.shape}")
        if not isinstance(fa.layout, mgpu.WGSplatFragLayout):
          raise ValueError(f"Expected WGSplatFragLayout, but got {fa.layout}")
        value = fa.registers.item()
        ir_ret.append(value)

    mgpu.dialect.return_(ir_ret)

