
def _mgpu_wgmma_op_lowering_rule(
    ctx: LoweringContext, wgmma_op: mgpu.WGMMAOp
) -> Sequence[ir.Value]:
  del ctx
  in_layouts = inference_utils.in_layouts(wgmma_op)
  assert in_layouts[0] == layouts_lib.to_layout_attr(fa.WGMMA_LAYOUT)
  [out_layout] = inference_utils.out_layouts(wgmma_op)
  assert out_layout == layouts_lib.to_layout_attr(fa.WGMMA_LAYOUT)

  # s8/i8 WGMMA expects signed integer accumulator.
  element_type = wgmma_op.a.type.element_type
  is_signed = True if isinstance(element_type, ir.IntegerType) else None
  regs = _fragmented_array_from_ir(
      wgmma_op.accumulator, in_layouts[0], is_signed
  )
  acc = wgmma.WGMMAAccumulator.from_registers(regs, sync=False)  # pyrefly: ignore[missing-attribute]

  if isinstance(wgmma_op.a.type, ir.VectorType):
    a_transforms = None
    b_transforms = inference_utils.in_transforms(wgmma_op)[0]
    unwrapped_a_ref = None
    unwrapped_b_ref = unwrap_transformed_memref(wgmma_op.b, b_transforms)
  else:
    a_transforms, b_transforms = inference_utils.in_transforms(wgmma_op)
    unwrapped_a_ref = unwrap_transformed_memref(wgmma_op.a, a_transforms)
    unwrapped_b_ref = unwrap_transformed_memref(wgmma_op.b, b_transforms)

  b_swizzle = swizzle_from_transforms_attr(b_transforms)

  if isinstance(wgmma_op.a.type, ir.VectorType):
    expected_a_layout = (
        fa.WGMMA_LAYOUT_8BIT
        if utils.bitwidth(element_type) == 8
        else fa.WGMMA_LAYOUT
    )
    assert in_layouts[1] == layouts_lib.to_layout_attr(expected_a_layout)
    a_operand = _fragmented_array_from_ir(wgmma_op.a, in_layouts[1], is_signed)
  else:
    assert a_transforms is not None
    a_swizzle = swizzle_from_transforms_attr(a_transforms)
    if a_swizzle != b_swizzle:
      raise ValueError(
          f"Non-matching swizzles of operands a and b in WGMMA: {a_swizzle} !="
          f" {b_swizzle}"
      )
    assert unwrapped_a_ref is not None
    a_operand = unwrapped_a_ref

  # pyrefly: ignore[missing-attribute]
  new_acc = wgmma.wgmma(acc, a_operand, unwrapped_b_ref, swizzle=b_swizzle)
  return [
      fragmented_array_to_ir(
          new_acc.value.to_layout(fa.WGMMA_LAYOUT),
          wgmma_op.accumulator.type,
      )
  ]

