
def _load_32xcols(base_addr, cols, dtype, tmem_packing) -> np.ndarray:
  i32 = ir.IntegerType.get_signless(32)
  vec_ty = ir.VectorType.get((2,), dtype)
  reg_packing = 32 // utils.bitwidth(dtype)
  if reg_packing == 1:
    load_shape = "16x256b"  # 4 threads * 64 bits per vreg = 256 bits
    assert tmem_packing == 1
    pack = False
  elif reg_packing == 2:
    load_shape = "16x128b"  # 4 threads * 32 bits per vreg = 128 bits
    assert 1 <= tmem_packing <= 2
    pack = tmem_packing == 1
  else:
    raise NotImplementedError(reg_packing)

  vector_regs = np.ndarray((4, cols // 8), dtype=object)

  it = _transfer_32xcols(base_addr, cols, (16, 8), tmem_packing, reg_packing)
  c0 = arith.constant(i32, 0)
  c1 = arith.constant(i32, 1)
  for addr_row_col, instr_num, lane_step, num_slice in it:
    regs = _tmem_load(addr_row_col, load_shape, instr_num, pack)
    row_slice = slice(lane_step * 2, (lane_step + 1) * 2)
    # This aliases the original array, so updates will be reflected there.
    vector_regs_update = vector_regs[row_slice, num_slice]
    assert vector_regs_update.shape == (2, instr_num), (vector_regs_update.shape, instr_num)
    if reg_packing == 1:
      regs = [llvm.bitcast(dtype, r) for r in regs]
      # From a single lane perspective a num tile consists of a 2x2, with the
      # minor dim traversing columns and major being 8 rows apart.
      # See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-fragments-shape-16256b
      regs = np.asarray(regs, dtype=object).reshape(instr_num, 2, 2).swapaxes(0, 1)
      undef = llvm.mlir_undef(vec_ty)
      assert regs.shape == (*vector_regs_update.shape, 2)
      for idx in np.ndindex(vector_regs_update.shape):
        high_undef = llvm.insertelement(undef, regs[(*idx, 0)], c0)
        vreg = llvm.insertelement(high_undef, regs[(*idx, 1)], c1)
        vector_regs_update[idx] = vreg
    else:
      assert reg_packing == 2
      regs = [llvm.bitcast(vec_ty, r) for r in regs]
      # From a single lane perspective a num tile has 2 registers, 8 rows apart.
      # See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-fragments-shape-16128b
      regs = np.asarray(regs, dtype=object).reshape(instr_num, 2).swapaxes(0, 1)
      vector_regs_update[...] = regs

  return vector_regs

