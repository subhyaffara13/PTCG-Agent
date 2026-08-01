
def mma(accumulator: _ods_ir.Value[_ods_ir.VectorType], a: _ods_ir.Value[_ods_ir.VectorType], b: _ods_ir.Value[_ods_ir.VectorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MMAOp(accumulator=accumulator, a=a, b=b, results=results, loc=loc, ip=ip).result


def mma(
    acc: fa.FragmentedArray,
    a: fa.FragmentedArray,
    b: fa.FragmentedArray,
) -> fa.FragmentedArray:
  """Computes `acc + a @ b` using synchronous warp-level MMA instructions.

  All operands must have `TiledLayout`s. The layouts must be generated
  by the `MMALayouts` class, which ensures that the tiles are mapped
  to the warps correctly.

  Args:
    acc: A `FragmentedArray` with a `TiledLayout` generated from
      `MMALayouts.acc`.
    a: A `FragmentedArray` with a `TiledLayout`  generated from
      `MMALayouts.lhs`.
    b: A `FragmentedArray` with a `TiledLayout` generated from `MMALayouts.rhs`.

  Returns:
    A new `FragmentedArray` with the result of the computation with
      the same type as `acc`.
  """

  (m, k) = a.shape
  (k2, n) = b.shape
  (m2, n2) = acc.shape

  if m != m2:
    raise ValueError(f"M mismatch: {m} != {m2}")
  if n != n2:
    raise ValueError(f"N mismatch: {n} != {n2}")
  if k != k2:
    raise ValueError(f"K mismatch: {k} != {k2}")

  # todo(cperivol): A tile shape can have dimensions that are higher
  # multiples of the mma op size as long as those dimensions are not
  # sharded across warps.
  i4 = ir.IntegerType.get_signless(4)
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)
  bf16 = ir.BF16Type.get()
  f16 = ir.F16Type.get()
  f8e4m3fn = ir.Float8E4M3FNType.get()
  f8e5m2 = ir.Float8E5M2Type.get()
  if (element_type := a.mlir_dtype) != b.mlir_dtype:
    raise ValueError(f"Dtype mismatch: {a.mlir_dtype} != {b.mlir_dtype}")
  if element_type not in (bf16, f16, f8e4m3fn, f8e5m2, i8, i4):
    raise NotImplementedError(f"Unsupported operand type: {element_type}")
  if isinstance(element_type, ir.IntegerType):
    if acc.mlir_dtype != i32:
      raise NotImplementedError("Only s32 accumulator supported for integer operands.")
    if not acc.is_signed:
      raise ValueError("Only signed accumulator supported for integer operands.")
  elif acc.mlir_dtype != ir.F32Type.get():
    raise NotImplementedError("Only f32 accumulator supported for floating operands.")

  layouts = MMALayouts(element_type)
  if layouts.lhs != a.layout:
    raise ValueError("Expected MMALayouts.lhs layout for A")
  if layouts.rhs != b.layout:
    raise ValueError("Expected MMALayouts.rhs layout for B")
  if layouts.acc != acc.layout:
    raise ValueError("Expected MMALayouts.acc layout for acc")

  assert isinstance(a.layout, fa.TiledLayout)
  assert isinstance(b.layout, fa.TiledLayout)
  assert isinstance(acc.layout, fa.TiledLayout)
  m_tile, k_tile = a.layout.base_tile_shape
  k_tile2, n_tile = b.layout.base_tile_shape
  m_tile2, n_tile2 = acc.layout.base_tile_shape

  assert k_tile == k_tile2
  assert m_tile2 == m_tile
  assert n_tile2 == n_tile

  num_m_tiles, num_n_tiles, num_k_tiles = m // m_tile, n // n_tile, k // k_tile

  # Do not modify the accumualtor itself.
  acc = acc.copy()
  s = lambda idx, length: slice(idx * length, (idx + 1) * length)
  for k_idx in range(num_k_tiles):
    for m_idx in range(num_m_tiles):
      for n_idx in range(num_n_tiles):
        ms = s(m_idx, m_tile)
        ns = s(n_idx, n_tile)
        ks = s(k_idx, k_tile)
        acc[ms, ns] = _mma_single_tile(acc[ms, ns], a[ms, ks], b[ks, ns])

  return acc


def mma(
    d: TMEMRef,
    a: ir.Value | TMEMRef,
    b: ir.Value,
    *,
    a_swizzle: int = 128,
    b_swizzle: int = 128,
    a_scale: TMEMRef | None = None,
    b_scale: TMEMRef | None = None,
    a_sparse_metadata: TMEMRef | None = None,
    accumulate: ir.Value | bool = True,
    collective: bool = False,
) -> None:
  if a_swizzle == 16 or b_swizzle == 16:
    raise NotImplementedError("No swizzle is not supported")
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)
  if isinstance(accumulate, bool):
    accumulate = arith.constant(ir.IntegerType.get_signless(1), accumulate)
  num_cta = 2 if collective else 1
  if (is_scaled := a_scale is not None) != (b_scale is not None):
    raise ValueError("Either none or both scales should be provided")
  is_sparse = a_sparse_metadata is not None
  if is_scaled and is_sparse:
    if isinstance(a, TMEMRef):
      raise NotImplementedError(
          "A in TMEM unsupported for block-scaled sparse matmuls"
      )

  # Step 1. Establish the shape and element type of the operation.
  if not isinstance(b.type, ir.MemRefType):
    raise ValueError(f"B must be a memref, got: {b.type}")
  (k, n), element_type = mma_utils.tiled_memref_shape(b)
  if isinstance(a, TMEMRef):
    m, k2 = a.shape
    element_type2 = a.dtype
    if is_scaled:
      raise NotImplementedError(
          "A in TMEM unsupported for block-scaled matmuls"
      )
    if m != 128:
      raise NotImplementedError(f"Only M=128 is supported for MMA with A in TMEM, but got M={m}")
    # Watch out: this layout must be consistent with D's layout (up to packing).
    expected_packing = 32 // utils.bitwidth(element_type)
    expected_layout = _infer_tmem_layout(
        a.shape, collective, packing=expected_packing
    )
    if a.layout != expected_layout:
      raise ValueError(
          f"A layout mismatch: expected {expected_layout}, got {a.layout}"
      )
  else:
    if not isinstance(a.type, ir.MemRefType):
      raise ValueError(f"A must be a memref, got {a.type}")
    (m, k2), element_type2 = mma_utils.tiled_memref_shape(a)
  if is_sparse:
    k2 *= 2
  if k != k2:
    raise ValueError(
        "MMA requires A and B to have the same contraction dimension (K),"
        f" got: {k2} and {k}"
    )
  if element_type != element_type2:
    raise ValueError(
        "MMA requires A and B to have the same element type, got:"
        f" {element_type2} and {element_type}"
    )
  if d.shape != (m, n * num_cta):
    raise ValueError(
        f"Accumulator shape mismatch: expected {(m, n * num_cta)}, got {d.shape}"
    )
  if m == 128:
    if d.layout != (expected_d_layout := tmem_default_layout(packing=1)):
      raise ValueError(
          f"Accumulator layout mismatch: expected {expected_d_layout}, got {d.layout}"
      )
    n_lane_groups = 1
  elif m == 64:
    if is_scaled and not collective:
      raise NotImplementedError("MMA with block scaling is not supported for 1CTA M=64")
    if is_sparse:
      raise NotImplementedError("Sparse MMA not supported for M=64")
    # Watch out: this layout must be consistent with A's layout (up to packing).
    # 2CTA M=128 instruction uses a different TMEM layout than 1CTA M=64.
    expected_d_layout = _infer_tmem_layout(d.shape, collective, packing=1)
    if d.layout != expected_d_layout:
      raise ValueError(
          f"Accumulator layout mismatch: expected {expected_d_layout}, got {d.layout}"
      )
    if collective:
      n_lane_groups = 1
    else:
      n_lane_groups = 2
      # We can't split N into groups if we would partition it below the tile size.
      # TODO: We only need to check this if N is the minormost dim in B.
      if 8 * b_swizzle // utils.bitwidth(element_type) > n // n_lane_groups:
        raise ValueError(
            f"Swizzle={b_swizzle} is too big for MMA with M=64. Try"
            " lowering it."
        )
  else:
    raise ValueError(f"Only M=128 and M=64 are supported for MMA, but got M={m}")
  f32 = ir.F32Type.get()
  f16 = ir.F16Type.get()
  s32 = ir.IntegerType.get_signless(32)
  if element_type == f32 or element_type == ir.BF16Type.get():
    if element_type == f32 and is_sparse:
      raise NotImplementedError("Sparse MMA unsupported for f32")
    if is_scaled:
      raise ValueError(
          f"MMA with element type {element_type} does not support block scaling"
      )
    if d.dtype != f32:
      raise ValueError(
          f"MMA with element type {element_type} only supports accumulators"
          f" of type f32, but got: {d.dtype}"
      )
  elif element_type == f16:
    if is_scaled:
      raise ValueError(
          f"MMA with element type {element_type} does not support block scaling"
      )
    if d.dtype != f16 and d.dtype != f32:
      raise ValueError(
          f"MMA with element type {element_type} only supports accumulators of"
          f" type f32 or f16, but got: {d.dtype}"
      )
  elif any(
      isinstance(element_type, t)
      for t in {ir.Float8E5M2Type, ir.Float8E4M3FNType}
  ):
    if d.dtype != f16 and d.dtype != f32:
      raise ValueError(
          f"MMA with element type {element_type} only supports accumulators of"
          f" type f32 or f16, but got: {d.dtype}"
      )
    if is_scaled and d.dtype != f32:
      raise ValueError(
          f"Block-scaled MMA with element type {element_type} only supports f32"
          f" accumulators, but got: {d.dtype}"
      )
  elif any(isinstance(element_type, t) for t in {ir.Float4E2M1FNType}):
    if not is_scaled:
      raise ValueError(
          f"MMA with element type {element_type} only supports block scaling"
      )
    if d.dtype != f32:
      raise ValueError(
          f"Block-scaled MMA with element type {element_type} only supports f32"
          f" accumulators, but got: {d.dtype}"
      )
  elif element_type == i8:
    if is_scaled:
      raise ValueError(
          f"MMA with element type {element_type} does not support block scaling"
      )
    if d.dtype != s32:
      raise ValueError(
          "MMA with element type s8 only supports s32 accumulators, but got:"
          f" {d.dtype}"
      )
  else:
    raise NotImplementedError(f"Unsupported element type: {element_type}")

  # Step 2. Decide on the instruction shapes we'll use. Note that with swizzles,
  # instructions must be issued in groups that are a multiple of swizzle.
  m_group_elems = m  # We have already verified M is supported above.
  k_group_elems = 8 * max(a_swizzle * (1 + is_sparse), b_swizzle) // utils.bitwidth(element_type)
  if is_sparse and k_group_elems < 64:
    # This is a limitation of the implementation below. We could relax it if we
    # ever need to support k=32.
    k_group_elems = 64
  scale_block: int | None = None
  if is_scaled:
    assert a_scale is not None
    scale_block = 32 if a_scale.dtype == ir.Float8E8M0FNUType.get() else 16
    if is_sparse:
      scale_block *= 2
    k_group_elems = max(k_group_elems, 4 * scale_block)
  required_multiple = 16 if collective else 8
  mode_name = "2 CTA" if collective else "1 CTA"
  if d.dtype == s32:
    required_multiple *= 2
    mode_name += " integer"
  if n_lane_groups > 1:
    mode_name += f" with {n_lane_groups} lane groups"
  if (n // n_lane_groups) % required_multiple != 0:
    raise ValueError(
        f"In {mode_name} MMA, N must be a multiple of {required_multiple},"
        f" got N={n}"
    )
  if is_sparse:
    n_div = 32 if collective and element_type == i8 else 16
    if n % n_div != 0:
      raise NotImplementedError(
          f"N must be a multiple of {n_div} for sparse MMA, but got N={n}"
      )
  if is_scaled and n % 32 != 0:
    raise NotImplementedError(
        "N must be a multiple of 32 for block-scaled MMA, but got N={n}"
    )
  if n > 256 and n.bit_count() != 1:
    raise NotImplementedError(f"The only supported N > 256, is 512, but got N={n}")
  # TODO: We could relax those constraints if we have multiple n_lane_groups,
  # since we will be unrolling the instructions anyway.
  if collective and n > 128:
    raise ValueError("Only N <= 128 are supported for collective MMA")
  elif n > 512:
    raise ValueError("Only N <= 512 are supported for MMA")
  n_group_elems = min(n // n_lane_groups, 256 // num_cta)
  if m % m_group_elems:
    raise ValueError(f"M must be a multiple of {m_group_elems}, got: {m}")
  if k % k_group_elems:
    raise ValueError(f"K must be a multiple of {k_group_elems}, got: {k}")
  if n % n_group_elems:
    raise ValueError(f"N must be a multiple of {n_group_elems}, got: {n}")
  m_groups = m // m_group_elems
  k_groups = k // k_group_elems
  n_groups = n // n_group_elems
  # TODO(apaszke): Require users to bitcast input refs to tf32 before MMA.
  mma_element_type = (
      ir.FloatTF32Type.get() if element_type == ir.F32Type.get() else element_type
  )

  # Check that the shapes and element types are correct for block scaling.
  scale_element_type = None
  if is_scaled:
    if n % 32:
      raise ValueError(
          f"MMA with block scaling requires N to be divisible by 32, got: {n}"
      )
    assert a_scale is not None and b_scale is not None
    scale_element_type = a_scale.dtype
    if (
        a_scale.dtype != ir.Float8E8M0FNUType.get()
        and a_scale.dtype != ir.Float8E4M3FNType.get()
    ):
      raise ValueError(
          f"A scale dtype mismatch: expected f8e8m0fnu or f8e4m3fn, got {a_scale.dtype}"
      )
    if b_scale.dtype != a_scale.dtype:
      raise ValueError(
          f"B scale dtype mismatch: expected {a_scale.dtype} (same as A), got"
          f" {b_scale.dtype}"
      )
    k_scales = k // scale_block
    if a_scale.shape != (TMEM_ROWS, k_scales):
      raise ValueError(
          f"A scale shape mismatch: expected ({TMEM_ROWS}, {k_scales}), got"
          f" {a_scale.shape}"
      )
    if a_scale.layout != scales_layout():
      raise ValueError(f"A scale layout {a_scale.layout} is not supported")
    if collective and m == 64:
      if b_scale.layout != b_scales_m64_collective_layout():
        raise ValueError(
            "Expected B scales to have a M=64 collective layout, got"
            f" {b_scale.layout}"
        )
    elif m == 128:
      if b_scale.layout != scales_layout():
        raise ValueError(
            f"Expected B scales to have a M=128 layout, got {b_scale.layout}"
        )
    else:
      raise AssertionError("Should not happen")
    if b_scale.shape[0] % 128 or b_scale.shape[0] < n * num_cta:
      raise ValueError(
          f"B scale shape[0] must be a multiple of 128 and >= N={n * num_cta},"
          f" got {b_scale.shape[0]}"
      )
    if b_scale.shape[1] != k_scales:
      raise ValueError(
          f"B scale shape mismatch: expected ({b_scale.shape[0]}, {k_scales}),"
          f" got {b_scale.shape}"
      )
  if is_sparse:
    sparse_group_elems = 8 if utils.bitwidth(element_type) == 4 else 4
    # Each sparse group has 2 entries.
    expected_meta_k = k // sparse_group_elems * 2
    if a_sparse_metadata.shape != (m, expected_meta_k):
      raise ValueError(
          f"A sparse metadata shape mismatch: expected {(m, expected_meta_k)},"
          f" got {a_sparse_metadata.shape}"
      )
    if a_sparse_metadata.dtype != ir.IntegerType.get_signless(2):
      raise ValueError(
          "A sparse metadata dtype mismatch: expected i2, got"
          f" {a_sparse_metadata.dtype}"
      )

  # Step 3. Compute the operand descriptors.
  if not isinstance(a, TMEMRef):
    # Both dense and sparse matmul consume A with a K bytewidth of 32, only
    # the group size is halved when it's sparse.
    (
        (a_desc_base, a_k_instr_strides),
        (a_m_group_stride, a_k_group_stride),
        a_fastest,
    ) = mma_utils.create_descriptor(
        a,
        swizzle=a_swizzle,
        group_size=(m_group_elems, k_group_elems // (1 + is_sparse)),
        logical_k_major=False,
        mma_bytewidth_k=32,
        split_const=True,
    )
  else:
    a_fastest = mma_utils.Dim.K
    a_k_instr_strides = None
    a_m_group_stride = a_k_group_stride = a_desc_base = None
  (
      (b_desc_base, b_k_instr_strides),
      (b_n_group_stride, b_k_group_stride),
      b_fastest,
  ) = mma_utils.create_descriptor(
      b,
      swizzle=b_swizzle,
      group_size=(k_group_elems, n_group_elems),
      logical_k_major=True,
      mma_bytewidth_k=64 if is_sparse else 32,
      split_const=True,
  )

  if is_scaled and utils.bitwidth(mma_element_type) == 4:
    if a_fastest != mma_utils.Dim.K:
      raise ValueError(
          "4-bit block scaled MMA only supports K-fastest operands, but A is M-fastest"
      )
    if b_fastest != mma_utils.Dim.K:
      raise ValueError(
          "4-bit block scaled MMA only supports K-fastest operands, but B is N-fastest"
      )
  if is_sparse:
    if b_swizzle == 32 and b_fastest == mma_utils.Dim.K:
      raise NotImplementedError(
          "B tiling too small. Increase swizzle or transpose the input."
      )

  # Step 4. Issue the instructions.
  true = arith.constant(ir.IntegerType.get_signless(1), 1)
  n_collective_group_elems = n_group_elems * num_cta
  n_col_groups = n_groups // n_lane_groups
  assert d.layout.base_tile_shape[0] % 4 == 0
  lanes_per_n_group = d.layout.base_tile_shape[0] // 4
  a_sparse_addr_base = a_sparse_metadata.address if is_sparse else None
  a_scale_addr_base = a_scale.address if is_scaled else None  # pyrefly: ignore[missing-attribute]
  b_scale_addr_base = b_scale.address if is_scaled else None  # pyrefly: ignore[missing-attribute]
  # B scales are padded when N is short, so it can't be derived from n_collective_group_elems.
  # Same for A scales when M is short.
  if is_scaled:
    assert isinstance(a_scale, TMEMRef) and isinstance(b_scale, TMEMRef)
    a_scale_m_stride = a_scale.layout.cols_in_shape((a_scale.shape[0], 4), bitwidth=8)
    b_scale_n_stride = b_scale.layout.cols_in_shape((b_scale.shape[0], 4), bitwidth=8)
  else:
    a_scale_m_stride = b_scale_n_stride = None
  for mi, ni, ki in np.ndindex(m_groups, n_groups, k_groups):
    if isinstance(a, TMEMRef):
      if m_groups != 1:
        raise NotImplementedError("A address calculation for multiple M tiles")
      a_k_group_elems = k_group_elems // (1 + is_sparse)
      a_mk = a.slice(slice(None), utils.ds(ki * a_k_group_elems, a_k_group_elems)).address
    else:
      assert a_desc_base is not None
      a_offset = mi * a_m_group_stride + ki * a_k_group_stride
      a_mk = (a_desc_base[0], a_desc_base[1] + mma_utils.encode_addr(a_offset))
    b_offset = ni * b_n_group_stride + ki * b_k_group_stride
    b_nk = (b_desc_base[0], b_desc_base[1] + mma_utils.encode_addr(b_offset))
    if a_sparse_addr_base is not None:
      if n_groups != 1 or m_groups != 1:
        raise NotImplementedError("A sparse metadata address calculation for multiple tiles")
      sparse_group_elems = 8 if utils.bitwidth(mma_element_type) == 4 else 4
      # Each sparse group has 2 entries, each TMEM column holds 16 i2 entries.
      cols_per_k_group = k_group_elems // sparse_group_elems * 2 // 16
      a_sparse_addr = arith.addi(a_sparse_addr_base, utils.c(ki * cols_per_k_group, i32))
    else:
      a_sparse_addr = None
    if a_scale_addr_base is not None and b_scale_addr_base is not None:
      if m_groups != 1:
        raise NotImplementedError("A scale address calculation for multiple M tiles")
      if n_groups != 1:
        raise NotImplementedError("B scale address calculation for multiple N tiles")
      assert scale_block is not None  # For type checkers.
      assert k_group_elems % (scale_block * 4) == 0
      assert m_group_elems % 32 == 0 and n_group_elems % 32 == 0
      k_scales_per_group = k_group_elems // (scale_block * 4)
      a_scale_addr = arith.addi(
          a_scale_addr_base,
          utils.c(ki * k_scales_per_group * a_scale_m_stride, i32),
      )
      b_scale_addr = arith.addi(
          b_scale_addr_base,
          utils.c(ki * k_scales_per_group * b_scale_n_stride, i32)
      )
    else:
      a_scale_addr = b_scale_addr = None
    acc = accumulate if ki == 0 else true
    ni_lane_group, ni_col = ni // n_col_groups, ni % n_col_groups
    d_offset = (
        ((ni_lane_group * lanes_per_n_group) << 16)
        + ni_col * n_collective_group_elems
    )
    if m_groups != 1:
      raise NotImplementedError("D address calculation for multiple M tiles")
    _do_mma(
        arith.addi(d.address, arith.constant(i32, d_offset)),
        a_mk,
        b_nk,
        d_type=d.dtype,
        m=m_group_elems,
        n=n_group_elems,
        k=k_group_elems,
        collective=collective,
        a_transpose=a_fastest != mma_utils.Dim.K,
        b_transpose=b_fastest != mma_utils.Dim.K,
        a_k_strides=a_k_instr_strides,
        b_k_strides=b_k_instr_strides,
        a_scale_addr=a_scale_addr,
        b_scale_addr=b_scale_addr,
        b_scale_n_stride=b_scale_n_stride,
        a_scale_m_stride=a_scale_m_stride,
        a_sparse_addr=a_sparse_addr,
        accumulate=acc,
        element_type=mma_element_type,
        scale_element_type=scale_element_type,
    )

