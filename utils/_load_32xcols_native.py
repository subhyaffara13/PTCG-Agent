
def _load_32xcols_native(base_addr, cols, dtype, tmem_packing, vector_length) -> np.ndarray:
  i32 = ir.IntegerType.get_signless(32)
  vec_ty = ir.VectorType.get((vector_length,), dtype)
  reg_packing = 32 // utils.bitwidth(dtype)
  assert vector_length % reg_packing == 0
  load_shape = "32x32b"
  load_atom_shape = (32, reg_packing)
  if reg_packing == 2:
    assert 1 <= tmem_packing <= 2
    pack = tmem_packing == 1
  else:
    if tmem_packing != reg_packing:
      raise NotImplementedError(
          f"Only {reg_packing} supported for element type {dtype}, but got"
          f" TMEM packing of {tmem_packing}"
      )
    pack = False

  it = _transfer_32xcols(base_addr, cols, load_atom_shape, tmem_packing, reg_packing)
  c0 = arith.constant(i32, 0)
  c1 = arith.constant(i32, 1)
  regs = [None] * (cols // reg_packing)
  for addr_row_col, instr_num, lane_step, num_slice in it:
    assert lane_step == 0, lane_step
    instr_regs = _tmem_load(addr_row_col, load_shape, instr_num, pack)
    if reg_packing == 1 and vector_length == 2:
      regs[num_slice] = [llvm.bitcast(dtype, r) for r in instr_regs]
    else:
      regs[num_slice] = [utils.bitcast(r, vec_ty) for r in instr_regs]

  if reg_packing == 1 and vector_length == 2:
    vector_regs = np.ndarray((cols // 2,), dtype=object)
    undef = llvm.mlir_undef(vec_ty)
    for idx in range(vector_regs.size):
      high_undef = llvm.insertelement(undef, regs[2 * idx], c0)
      vreg = llvm.insertelement(high_undef, regs[2 * idx + 1], c1)
      vector_regs[idx] = vreg
  else:
    assert vector_length == reg_packing
    vector_regs = np.asarray(regs, dtype=object)

  return vector_regs

