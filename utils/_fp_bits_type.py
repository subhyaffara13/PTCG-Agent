
def _fp_bits_type(t: ir.Type) -> ir.Type:
  if isinstance(t, ir.RankedTensorType):
    t_type = ir.RankedTensorType(t)
    return ir.RankedTensorType.get(
      t_type.shape, _fp_bits_type(t_type.element_type), t_type.encoding
    )
  elif _is_triton_pointer_type(t):
    ptr_type = tt_dialect.PointerType(t)
    return tt_dialect.PointerType.get(
      _fp_bits_type(ptr_type.pointee_type), ptr_type.address_space
    )
  else:
    assert isinstance(t, ir.FloatType)
    return ir.IntegerType.get_signless(t.width)

