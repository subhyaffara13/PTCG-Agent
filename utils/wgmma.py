from typing import Any

def wgmma(accumulator: _ods_ir.Value[_ods_ir.VectorType], a: _ods_ir.Value, b: _ods_ir.Value[_ods_ir.MemRefType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return WGMMAOp(accumulator=accumulator, a=a, b=b, results=results, loc=loc, ip=ip).result


def wgmma(acc: gpu_core.WGMMAAbstractAccumulatorRef, a, b) -> None:
  """Performs an asynchronous warp group matmul-accumulate on the given references.

  Conceptually, this is equivalent to doing ``acc[...] += a[...] @ b[...]``,
  except that the computation is performed asynchronously.

  Args:
    acc: The accumulator reference. Needs to be allocated via
      :func:`jax.experimental.pallas.run_scoped` called with a
      :func:`jax.experimental.pallas.mosaic_gpu.WGMMAAccumulatorRef`.
    a: The left hand side operand reference.
    b: The right hand side operand reference.

  See also:
    :func:`jax.experimental.pallas.mosaic_gpu.wgmma_wait`
  """
  m, n = acc.shape
  m2, k = a.shape
  k2, n2 = b.shape

  if m != m2 or n != n2 or k != k2:
    raise ValueError(
        f"Incompatible shapes for matrix multiplication: lhs={a.shape},"
        f" rhs={b.shape=}, acc={acc.shape}"
    )

  if a.dtype != b.dtype:
    raise ValueError(f"Mixed input dtypes for matrix multiplication unsupported: lhs={a.dtype}, rhs={b.dtype}")

  acc_transforms_leaves: list
  if isinstance(acc, pallas_core.TransformedRef):
    acc_transforms_leaves, acc_transforms_tree = jax.tree.flatten(acc.transforms)
    acc = acc.ref
  else:
    acc_transforms_leaves, acc_transforms_tree = [], None

  if isinstance(a, pallas_core.TransformedRef):
    a_transforms_leaves, a_transforms_tree = jax.tree.flatten(a.transforms)
    a = a.ref
  else:
    a_transforms_leaves, a_transforms_tree = [], None

  if isinstance(b, pallas_core.TransformedRef):
    b_transforms_leaves, b_transforms_tree = jax.tree.flatten(b.transforms)
    b = b.ref
  else:
    b_transforms_leaves, b_transforms_tree = [], None

  wgmma_ref_p.bind(
      acc,
      a,
      b,
      *acc_transforms_leaves,
      *a_transforms_leaves,
      *b_transforms_leaves,
      acc_transforms_tree=acc_transforms_tree,
      a_transforms_tree=a_transforms_tree,
      b_transforms_tree=b_transforms_tree,
  )


def wgmma(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    acc_allocation_key_as_array: jax.Array,
    acc_transforms: tuple[Any, ...],
    acc_dtype: jnp.dtype,
    a_allocation_key_as_array: jax.Array,
    a_transforms: tuple[Any, ...],
    b_allocation_key_as_array: jax.Array,
    b_transforms: tuple[Any, ...],
    source_info: source_info_util.SourceInfo | None = None,
):
  # TODO(jburnim): Vector clocks.
  # TODO(jburnim): Async wgmma.

  device_id: int = int(device_id)  # pyrefly: ignore[redefinition]
  grid_point_coords: tuple[int, ...] = tuple(int(x) for x in grid_point_coords)  # pyrefly: ignore[redefinition]
  thread_id: int = int(thread_id)  # pyrefly: ignore[redefinition]
  acc_allocation_key = HostAllocationKey.from_array(acc_allocation_key_as_array)
  a_allocation_key = HostAllocationKey.from_array(a_allocation_key_as_array)
  b_allocation_key = HostAllocationKey.from_array(b_allocation_key_as_array)
  a_transforms = jax.tree.map(int, _remove_noop_transforms(a_transforms))  # pyrefly: ignore[redefinition]
  b_transforms = jax.tree.map(int, _remove_noop_transforms(b_transforms))  # pyrefly: ignore[redefinition]
  acc_transforms = jax.tree.map(int, _remove_noop_transforms(acc_transforms))  # pyrefly: ignore[redefinition]

  shared_memory = _get_shared_memory()
  global_thread_id = shared_memory.get_global_thread_id(device_id, thread_id)

  logging_info = interpret_utils.GPULoggingInfo(
      device_id=device_id,
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      source_info=source_info,
  )

  a, _, _ = shared_memory.get_buffer_content(
      a_allocation_key, interpret_utils.to_range(a_transforms),
      global_thread_id, logging_info=logging_info)
  b, _, _ = shared_memory.get_buffer_content(
      b_allocation_key, interpret_utils.to_range(b_transforms),
      global_thread_id, logging_info=logging_info)
  assert a is not None
  assert b is not None
  acc_range = interpret_utils.to_range(acc_transforms)
  acc, _, _ = shared_memory.get_buffer_content(
      acc_allocation_key, acc_range, global_thread_id,
      logging_info=logging_info)

  res = acc + np.matmul(a, b, dtype=acc_dtype)

  shared_memory.store_buffer_content(
      acc_allocation_key, acc_range, res,
      global_thread_id, logging_info=logging_info)

  return token


def wgmma(
    acc: WGMMAAccumulator,
    a: fa.FragmentedArray | ir.Value,
    b: ir.Value,
    *,
    swizzle: int = 128,
):
  """Perform acc += a @ b using the WGMMA instruction.

  `a` may be passed in registers, or as a memref. `b` must be a memref.

  The expected (logical) memref shapes are:
    a: (m // tile_m, k // tile_k, tile_m, tile_k)
    b: (k // tile_k, n // tile_n, tile_k, tile_n).

  While the shapes may be physically transposed, when considering the row-major
  physical shape, the tile dimensions must be the two minor dimensions and must
  have the shape (8, S) where S = swizzle // bytewidth(element_type).
  """
  if swizzle == 16:
    raise NotImplementedError("No swizzle is not supported")
  # Step 1. Establish the shape and element type of the operation.
  if not isinstance(b.type, ir.MemRefType):
    raise ValueError(f"B must be a memref, got: {b.type}")
  bf16 = ir.BF16Type.get()
  f32 = ir.F32Type.get()
  f16 = ir.F16Type.get()
  i32 = ir.IntegerType.get_signless(32)
  i8 = ir.IntegerType.get_signless(8)
  f8e5m2 = ir.Float8E5M2Type.get()
  f8e4m3fn = ir.Float8E4M3FNType.get()
  (k, n), element_type = mma_utils.tiled_memref_shape(b)
  if a_in_regs := isinstance(a, fa.FragmentedArray):
    m, k2 = a.shape
    element_type2 = a.mlir_dtype
    if element_type2 not in {f16, bf16, i8, f8e5m2, f8e4m3fn}:
      raise ValueError(
          "Only f16, bf16, i8, f8e5m2, f8e4m3fn are supported for A "
          f"in registers, got {element_type2}"
      )
    if element_type2 == i8 and swizzle == 32:
      # TODO(bchetioui): relax this when ptxas is fixed. As of ptxas 12.8,
      # optimizations eliminate MMA instructions, leading to only the first tile
      # of the result being computed correctly.
      raise NotImplementedError("swizzle=32 not supported for s8 lhs in registers")
  elif isinstance(a.type, ir.MemRefType):
    (m, k2), element_type2 = mma_utils.tiled_memref_shape(a)
  else:
    raise ValueError(f"Unsupported A type: {type(a)}")
  if k != k2:
    raise ValueError(
        "WGMMA requires A and B to have the same contraction dimension (K),"
        f" got: {k2} and {k}"
    )
  if element_type != element_type2:
    raise ValueError(
        "WGMMA requires A and B to have the same element type, got:"
        f" {element_type2} and {element_type}"
    )
  if acc._value.shape != (m, n):
    raise ValueError(
        f"Accumulator shape mismatch: expected {(m, n)}, got {acc._value.shape}"
    )
  if element_type == f32 or element_type == ir.BF16Type.get():
    if acc._value.mlir_dtype != f32:
      raise ValueError(
          f"WGMMA with element type {element_type} only supports accumulators"
          f" of type f32, but got: {acc._value.mlir_dtype}"
      )
  elif any(
      isinstance(element_type, t)
      for t in {ir.F16Type, ir.Float8E5M2Type, ir.Float8E4M3FNType}
  ):
    if acc._value.mlir_dtype != f16 and acc._value.mlir_dtype != f32:
      raise ValueError(
          f"WGMMA with element type {element_type} only supports accumulators "
          f"of type f32 or f16, but got: {acc._value.mlir_dtype}"
      )
  elif element_type == i8:
    if a_in_regs and not a.is_signed:  # pyrefly: ignore[missing-attribute]
      raise NotImplementedError("WGMMA with lhs of type u8")
    if acc._value.mlir_dtype != i32 or not acc._value.is_signed:
      raise ValueError(
          f"WGMMA with element type {element_type} only supports accumulators "
          f"of type s32, but got: {acc._value.mlir_dtype}"
      )
  else:
    raise NotImplementedError(f"Unsupported element type: {element_type}")

  # Step 2. Decide on the instruction shapes we'll use. Note that with swizzles,
  # instructions must be issued in groups of the same width as the swizzle.
  m_group_elems = 64  # Hopper has a fixed M instruction shape.
  k_group_elems = swizzle // utils.bytewidth(element_type)
  if n > 256 or n % 8:
    raise ValueError(f"N must be a multiple of 8 and <= 256, got: {n}")
  n_group_elems = n  # We assume only one N group below.
  if m % m_group_elems:
    raise ValueError(f"M must be a multiple of {m_group_elems}, got: {m}")
  if k % k_group_elems:
    raise ValueError(f"K must be a multiple of {k_group_elems}, got: {k}")
  m_groups = m // m_group_elems
  k_groups = k // k_group_elems
  # TODO(apaszke): Require users to bitcast input refs to tf32 before WGMMA.
  wgmma_element_type = (
      ir.FloatTF32Type.get() if element_type == ir.F32Type.get() else element_type
  )

  # Step 3. Compute the operand descriptors.
  if a_in_regs:
    a_desc_base = a_m_group_stride = a_k_group_stride = None
    a_instr_params = dict(a_transpose=None, a_k_stride=None)
  else:
    assert isinstance(a, ir.Value)
    (
        (a_desc_base, a_k_instr_stride),
        (a_m_group_stride, a_k_group_stride),
        a_fastest,
    ) = mma_utils.create_descriptor(
        a,
        swizzle=swizzle,
        large_tile=(m_group_elems, k_group_elems),
        group_size=(m_group_elems, k_group_elems),
        logical_k_major=False,
    )
    assert not a_k_instr_stride[0]  # We'd need separate a/b swizzles.
    a_k_instr_stride = a_k_instr_stride[1][0]
    a_instr_params = dict(a_transpose=a_fastest != mma_utils.Dim.K,
                          a_k_stride=a_k_instr_stride)
  (
      (b_desc_base, b_k_instr_stride),
      (b_n_group_stride, b_k_group_stride),
      b_fastest,
  ) = mma_utils.create_descriptor(
      b,
      swizzle=swizzle,
      large_tile=(k_group_elems,) * 2,  # It's not a typo that we use k for n.
      group_size=(k_group_elems, n_group_elems),
      logical_k_major=True,
  )
  assert not b_k_instr_stride[0]  # We'd need separate a/b swizzles.
  b_k_instr_stride = b_k_instr_stride[1][0]
  del b_n_group_stride  # We only support one N group.

  # Step 4. Issue the instructions.
  if a_in_regs:
    assert isinstance(a, fa.FragmentedArray)
    a = wgmma_fence(a)  # Make sure the registers are ready.

  i64 = ir.IntegerType.get_signless(64)
  new_acc_regs = acc._value.registers.copy()
  for mi in range(m_groups):
    for ki in range(k_groups):
      if a_in_regs:
        assert isinstance(a, fa.FragmentedArray)
        a_mk = a[
            mi * m_group_elems : (mi + 1) * m_group_elems,
            ki * k_group_elems : (ki + 1) * k_group_elems,
        ]
      else:
        assert a_m_group_stride is not None and a_k_group_stride is not None
        a_group_offset = mi * a_m_group_stride + ki * a_k_group_stride
        a_mk = _llvm_add(
            a_desc_base, c(mma_utils.encode_addr(a_group_offset), i64),
        )
      b_k = _llvm_add(
          b_desc_base, c(mma_utils.encode_addr(ki * b_k_group_stride), i64)
      )
      new_acc_regs[mi : mi + 1] = wgmma_m64(
          new_acc_regs[mi : mi + 1],
          a_mk,
          b_k,
          swizzle=swizzle,
          n=n_group_elems,
          element_type=wgmma_element_type,
          b_transpose=b_fastest != mma_utils.Dim.K,
          b_k_stride=b_k_instr_stride,
          **a_instr_params,
      )
  return WGMMAAccumulator(
      _value=fa.FragmentedArray(
          _registers=new_acc_regs,
          _layout=acc._value.layout,
          _is_signed=acc._value.is_signed,
      ),
      _original_layout=acc._original_layout,
      _sync=False,
  )

