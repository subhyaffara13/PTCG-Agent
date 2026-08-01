
def _store_32xcols(base_addr, vector_regs, tmem_packing) -> None:
  i32 = ir.IntegerType.get_signless(32)
  assert vector_regs.ndim == 2 and vector_regs.shape[0] == 4
  cols = vector_regs.shape[1] * 8

  reg_packing = 64 // utils.bitwidth(vector_regs.flat[0].type)
  if reg_packing == 1:
    store_shape = "16x256b"  # 4 threads * 64 bits per vreg = 256 bits
    regs = np.empty((4, vector_regs.shape[1], 2), dtype=object)
    c0 = arith.constant(i32, 0)
    c1 = arith.constant(i32, 1)
    for idx, vreg in np.ndenumerate(vector_regs):
      regs[(*idx, 0)] = llvm.extractelement(vreg, c0)
      regs[(*idx, 1)] = llvm.extractelement(vreg, c1)
    regs = regs.reshape(2, 2, vector_regs.shape[1], 2).swapaxes(1, 2)
    # From a single lane perspective a num tile consists of a 2x2, with the
    # minor dim traversing columns and major being 8 rows apart.
    # See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-fragments-shape-16256b
    assert regs.shape[-2:] == (2, 2)
    assert tmem_packing == 1
    unpack = False
  elif reg_packing == 2:
    store_shape = "16x128b"  # 4 threads * 32 bits per vreg = 128 bits
    # From a single lane perspective a num tile has 2 registers, 8 rows apart.
    # See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-matrix-fragments-shape-16128b
    regs = vector_regs.reshape(2, 2, vector_regs.shape[1]).swapaxes(1, 2)
    assert 1 <= tmem_packing <= 2
    unpack = tmem_packing == 1
  else:
    raise NotImplementedError(reg_packing)

  it = _transfer_32xcols(base_addr, cols, (16, 8), tmem_packing, reg_packing)
  for addr_row_col, instr_num, lane_step, num_slice in it:
    regs_slice = regs[lane_step, num_slice].flat
    _tmem_store(addr_row_col, store_shape, instr_num, regs_slice, unpack)

