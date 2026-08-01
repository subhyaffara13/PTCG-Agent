
def _mma_single_tile(
    acc: fa.FragmentedArray, a: fa.FragmentedArray, b: fa.FragmentedArray
) -> fa.FragmentedArray:
  """Performs `acc + a @ b` using warp level MMA instructions."""
  i32 = ir.IntegerType.get_signless(32)

  k_tile = 256 // utils.bitwidth(a.mlir_dtype)
  assert a.shape == (64, k_tile)
  assert b.shape == (k_tile, 8)
  assert acc.shape == (64, 8)
  assert a.mlir_dtype == b.mlir_dtype
  is_integer = isinstance(a.mlir_dtype, ir.IntegerType)
  assert acc.mlir_dtype == i32 if is_integer else ir.F32Type.get()
  assert acc.is_signed in {None, True}
  assert (
      isinstance(acc.layout, fa.TiledLayout)
      and isinstance(a.layout, fa.TiledLayout)
      and isinstance(b.layout, fa.TiledLayout)
  )
  num_acc_regs, num_a_regs, num_b_regs = 4, 4, 2

  acc_regs = [
      vector.extract(
          reg,
          dynamic_position=[],
          static_position=ir.DenseI64ArrayAttr.get([pos]),
      )
      for reg in acc.registers.flatten()
      for pos in range(acc.layout.vector_length)
  ]
  a_regs = [utils.bitcast(r, i32) for r in a.registers.flatten()]
  b_regs = [utils.bitcast(r, i32) for r in b.registers.flatten()]

  # Make sure we have the right number of registers for the instruction.
  assert len(a_regs) == 4
  assert len(acc_regs) == 4
  assert len(b_regs) == 2

  a_ptx_dtype = _ptx_dtype_str(a.mlir_dtype, is_signed=a.is_signed)
  b_ptx_dtype = _ptx_dtype_str(b.mlir_dtype, is_signed=b.is_signed)
  acc_ptx_dtype = "s32" if is_integer else "f32"
  acc_constraint = "r" if is_integer else "f"
  instr = f"mma.sync.aligned.m16n8k{k_tile}.row.col.{acc_ptx_dtype}.{a_ptx_dtype}.{b_ptx_dtype}.{acc_ptx_dtype}"
  counter = itertools.count()
  n_regs_str = lambda n: (
      "{" + ",".join([f"${next(counter)}" for _ in range(n)]) + "}"
  )
  out_regs_str = n_regs_str(num_acc_regs)
  a_regs_str = n_regs_str(num_a_regs)
  b_regs_str = n_regs_str(num_b_regs)
  c_regs_str = n_regs_str(num_acc_regs)
  ptx = f"{instr} {out_regs_str}, {a_regs_str}, {b_regs_str}, {c_regs_str};"
  # See: https://llvm.org/docs/LangRef.html#inline-assembler-expressions
  constraints = (
      f"{','.join([f'={acc_constraint}']*num_acc_regs)},"
      f"{','.join(['r']*num_a_regs)},"
      f"{','.join(['r']*num_b_regs)},"
      f"{','.join([acc_constraint]*num_acc_regs)}"
  )

  in_operands = [*a_regs, *b_regs, *acc_regs]
  out_regs_struct = llvm.inline_asm(
      llvm.StructType.get_literal([acc.mlir_dtype] * len(acc_regs)),
      in_operands,
      ptx,
      constraints,
      has_side_effects=False,
  )
  assert isinstance(out_regs_struct, ir.Value)
  out_regs = [
      llvm.extractvalue(acc.mlir_dtype, out_regs_struct, [i])
      for i in range(len(acc_regs))
  ]
  vec_regs = []
  vec_undef = llvm.mlir_undef(ir.VectorType.get((2,), acc.mlir_dtype))
  for first, second in zip(out_regs[::2], out_regs[1::2]):
    vec = llvm.insertelement(vec_undef, first, position=utils.c(0, i32))
    vec = llvm.insertelement(vec, second, position=utils.c(1, i32))
    vec_regs.append(vec)
  out_regs = np.asarray(vec_regs, dtype=object).reshape(acc.registers.shape)
  return fa.FragmentedArray(
      _registers=out_regs, _layout=acc.layout, _is_signed=acc.is_signed
  )

