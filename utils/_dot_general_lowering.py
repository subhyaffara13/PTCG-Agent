
def _dot_general_lowering(
    ctx: LoweringRuleContext,
    a,
    b,
    *,
    dimension_numbers,
    out_sharding,
    precision,
    preferred_element_type,
):
  for aval in ctx.avals_in:
    if jnp.issubdtype(aval.dtype, jnp.unsignedinteger):
      raise NotImplementedError(
          f"Unsigned integer dtype {aval.dtype} is not supported for"
          " dot_general (matmul) on the Pallas Triton GPU backend because"
          " dot_general interprets all integer inputs as signed. Consider"
          " casting to a signed type before the dot operation."
      )
  del preferred_element_type, out_sharding  # Unused.
  ((a_contract_dim,), (b_contract_dim,)), batch_dims = dimension_numbers
  assert batch_dims == ((), ())

  if a_contract_dim == 0:
    a = tt_dialect.trans(a, (1, 0))
  if b_contract_dim == 1:
    b = tt_dialect.trans(b, (1, 0))

  a_aval, b_aval = ctx.avals_in
  [out_aval] = ctx.avals_out

  if precision is None or (precision == lax.DotAlgorithmPreset.DEFAULT):
    precision = (lax.Precision.DEFAULT, lax.Precision.DEFAULT)

  if isinstance(precision, lax.DotAlgorithmPreset):
    match precision:
      case lax.DotAlgorithmPreset.TF32_TF32_F32:
        input_precision = tt_dialect.InputPrecision.TF32
      case lax.DotAlgorithmPreset.TF32_TF32_F32_X3:
        input_precision = tt_dialect.InputPrecision.TF32x3
      case lax.DotAlgorithmPreset.F32_F32_F32:
        input_precision = tt_dialect.InputPrecision.IEEE
      case (
          lax.DotAlgorithmPreset.F16_F16_F16
          | lax.DotAlgorithmPreset.F16_F16_F32
          | lax.DotAlgorithmPreset.BF16_BF16_BF16
          | lax.DotAlgorithmPreset.BF16_BF16_F32
          | lax.DotAlgorithmPreset.BF16_BF16_F32_X3
          | lax.DotAlgorithmPreset.BF16_BF16_F32_X6
          | lax.DotAlgorithmPreset.BF16_BF16_F32_X9
      ):
        input_precision = None
      case _:
        raise NotImplementedError(f"Unsupported dot algorithm: {precision}.")

    assert precision.supported_lhs_types is not None
    assert precision.supported_rhs_types is not None
    a = _cast(a, a_aval.dtype, precision.supported_lhs_types[0])
    b = _cast(b, b_aval.dtype, precision.supported_rhs_types[0])
    acc_dtype = precision.accumulation_type
  elif isinstance(precision, tuple):
    a_precision, b_precision = precision
    if a_precision in _TF32_PRECISIONS or b_precision in _TF32_PRECISIONS:
      input_precision = tt_dialect.InputPrecision.TF32
    elif a_aval.dtype == jnp.float32:
      input_precision = tt_dialect.InputPrecision.IEEE
    else:
      input_precision = None

    acc_dtype = out_aval.dtype
    if acc_dtype not in (jnp.int32, jnp.float16, jnp.float64):
      acc_dtype = jnp.float32
  else:
    raise NotImplementedError(f"Unsupported dot precision: {precision}.")

  a_type = ir.RankedTensorType(a.type)
  b_type = ir.RankedTensorType(b.type)
  if len(a_type.shape) != 2 or len(b_type.shape) != 2:
    raise ValueError("a and b must be 2D, but got:"
                     f" {a_type.shape} and {b_type.shape}")

  m, k = a_type.shape
  _, n = b_type.shape
  if a_type.element_type == ir.F64Type.get():
    # Triton's MMAv2 fp64 path uses the m8n8k4 PTX instruction but aggregates
    # it with NumRegisters={m:2, n:1, k:4}, producing an effective m16n8k16
    # per-warp tile.  Blocks smaller than these minimums cause repM/repN/repK
    # to round to zero, corrupting the ValueTable and segfaulting the compiler.
    #   M >= 16  (2 × instrM=8)
    #   N >=  8  (1 × instrN=8)
    #   K >= 16  (4 × instrK=4)
    errors = []
    if m < 16:
      errors.append(f"M={m} < 16")
    if n < 8:
      errors.append(f"N={n} < 8")
    if k < 16:
      errors.append(f"K={k} < 16")
    if errors:
      raise ValueError(
          f"float64 dot requires M>=16, N>=8, K>=16 per warp tile "
          f"(Triton MMAv2 m8n8k4 layout); got {', '.join(errors)}"
      )

  if a_type.element_type != b_type.element_type:
    raise ValueError(
        "a and b must have the same element type, but got:"
        f" {a_type.element_type} and {b_type.element_type}"
    )

  assert acc_dtype is not None
  acc = _zeros(ir.RankedTensorType.get([m, n], _dtype_to_ir_type(acc_dtype)))

  if precision in (
      lax.DotAlgorithmPreset.BF16_BF16_F32_X3,
      lax.DotAlgorithmPreset.BF16_BF16_F32_X6,
      lax.DotAlgorithmPreset.BF16_BF16_F32_X9,
  ):
    a_bf16 = _as_bf16(a)
    b_bf16 = _as_bf16(b)
    a_err0 = _sub(a, _as_f32(a_bf16))
    b_err0 = _sub(b, _as_f32(b_bf16))
    a_err0_bf16 = _as_bf16(a_err0)
    b_err0_bf16 = _as_bf16(b_err0)
    a_err1_bf16 = _as_bf16(_sub(a_err0, _as_f32(a_err0_bf16)))
    b_err1_bf16 = _as_bf16(_sub(b_err0, _as_f32(b_err0_bf16)))
    # Accumulate the smallest values first to reduce the numeric error.
    if precision == lax.DotAlgorithmPreset.BF16_BF16_F32_X9:
      acc = tt_dialect.dot(a_err1_bf16, b_err0_bf16, acc)
      acc = tt_dialect.dot(a_err1_bf16, b_err1_bf16, acc)
      acc = tt_dialect.dot(a_err0_bf16, b_err1_bf16, acc)
    if precision in (
        lax.DotAlgorithmPreset.BF16_BF16_F32_X6,
        lax.DotAlgorithmPreset.BF16_BF16_F32_X9,
    ):
      acc = tt_dialect.dot(a_err1_bf16, b_bf16, acc)
      acc = tt_dialect.dot(a_bf16, b_err1_bf16, acc)
      acc = tt_dialect.dot(a_err0_bf16, b_err0_bf16, acc)
    acc = tt_dialect.dot(a_err0_bf16, b_bf16, acc)
    acc = tt_dialect.dot(a_bf16, b_err0_bf16, acc)
    # If `a` rounding error is zero and `b` is `inf` then `acc` may contain
    # `NaN`s (as `0 * inf = NaN`), and vice versa.
    acc = arith_dialect.select(_is_nan(acc), _zeros_like(acc), acc)
    a, b = a_bf16, b_bf16

  acc = tt_dialect.dot(a, b, acc, input_precision=input_precision)
  return _cast(acc, acc_dtype, out_aval.dtype)

