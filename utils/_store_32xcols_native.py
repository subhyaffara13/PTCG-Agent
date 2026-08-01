
def _store_32xcols_native(base_addr, vector_regs, tmem_packing) -> None:
  i32 = ir.IntegerType.get_signless(32)
  assert vector_regs.ndim == 1
  vec_ty = ir.VectorType(vector_regs.flat[0].type)
  [vector_length] = vec_ty.shape
  elt_bitwidth = utils.bitwidth(vec_ty.element_type)
  reg_packing = 32 // elt_bitwidth
  store_atom_shape = (32, reg_packing)
  # TODO(apaszke): More general register splitting code, not just 2x32b.
  if reg_packing == 1:
    if vector_length == 2:
      # Transform data such that each reg is 32 bits wide.
      regs: list[ir.Value | None] = [None] * (len(vector_regs) * 2)
      c0 = arith.constant(i32, 0)
      c1 = arith.constant(i32, 1)
      for idx, vreg in enumerate(vector_regs):
        regs[2 * idx] = llvm.extractelement(vreg, c0)
        regs[2 * idx + 1] = llvm.extractelement(vreg, c1)
    else:
      regs = [utils.bitcast(r, i32) for r in vector_regs]
    assert tmem_packing == 1
    unpack = False
  elif reg_packing == 2:
    assert vector_length == 2
    # In this case, registers are already packed into 32-bit registers.
    regs = [utils.bitcast(r, i32) for r in vector_regs]
    if elt_bitwidth == 16:
      assert 1 <= tmem_packing <= 2
      unpack = tmem_packing == 1
    else:
      if tmem_packing == 1 and elt_bitwidth != 32:
        raise NotImplementedError(
            f"Unsupported packing: {tmem_packing} for element type {elt_bitwidth}"
        )
      assert tmem_packing == 32 // elt_bitwidth
      unpack = False
  else:
    if tmem_packing != reg_packing:
      raise NotImplementedError(
          f"Only {reg_packing} packing supported for bitwidth {elt_bitwidth},"
          f" but got TMEM packing of {tmem_packing}"
      )
    assert utils.bitwidth(vec_ty) == 32
    regs = [utils.bitcast(r, i32) for r in vector_regs]
    unpack = False
  cols = len(regs) * reg_packing
  it = _transfer_32xcols(base_addr, cols, store_atom_shape, tmem_packing, reg_packing)
  for addr_row_col, instr_num, lane_step, num_slice in it:
    assert lane_step == 0
    regs_slice = regs[num_slice]
    _tmem_store(addr_row_col, "32x32b", instr_num, regs_slice, unpack)

