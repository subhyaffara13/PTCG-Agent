
def _tma_dma_type(
    element_type: ir.Type,
    reduction_op: TMAReductionOp | None,
) -> int:
  """Returns the TMA DMA type for the given element type and signedness."""
  if isinstance(element_type, ir.IntegerType):
    bitwidth = utils.bitwidth_impl(element_type)
    if bitwidth == 2:
      tma_dtype = 8
    elif bitwidth == 4:
      tma_dtype = 0
    elif bitwidth == 8:
      tma_dtype = 1
    elif bitwidth == 16:
      tma_dtype = 2
    elif bitwidth == 32:
      tma_dtype = 9 if reduction_op in ("smin", "smax") else 3
    elif bitwidth == 64:
      tma_dtype = 10 if reduction_op in ("smin", "smax") else 4
    else:
      raise ValueError(f"Unsupported integer bitwidth: {bitwidth}")
  elif isinstance(element_type, ir.F16Type):
    tma_dtype = 5
  elif isinstance(element_type, ir.F32Type):
    tma_dtype = 6
  elif isinstance(element_type, ir.BF16Type):
    tma_dtype = 7
  # We treat narrow floats as integers
  elif isinstance(element_type, ir.Float8E5M2Type):
    tma_dtype = 1
  elif isinstance(element_type, ir.Float8E4M3FNType):
    tma_dtype = 1
  elif isinstance(element_type, ir.Float8E8M0FNUType):
    tma_dtype = 1
  elif isinstance(element_type, ir.Float4E2M1FNType):
    tma_dtype = 0
  else:
    raise ValueError(f"unsupported TMA dtype {element_type}")
  return tma_dtype

