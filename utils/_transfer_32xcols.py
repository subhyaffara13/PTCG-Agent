
def _transfer_32xcols(
    base_addr: ir.Value,
    cols: int,
    atom_shape: tuple[int, int],
    tmem_packing: int,
    reg_packing: int,
) -> Iterator[tuple[ir.Value, int, int, slice]]:
  """Generates a sequence of parameters for a given TMEM read or write.

  Arguments:
    base_addr: The base address of the TMEM region.
    cols: The number of logical columns to transfer.
    atom_shape: The logical shape of the tile written by the warp in a single
      TMEM transfer.
    tmem_packing: Packing degree in TMEM. When packing is 1, but the data is
      16-bit, we expect that each transfer actually involves double the number
      of physical columns.
    reg_packing: The number of elements that fit in a single 32-bit register.
  """
  i32 = ir.IntegerType.get_signless(32)
  atom_rows, atom_cols = atom_shape
  assert cols % atom_cols == 0
  total_num = cols // atom_cols
  regs_per_instr = atom_shape[0] * atom_shape[1] // (utils.WARP_SIZE * reg_packing)
  assert 32 % atom_rows == 0
  num_row_steps = 32 // atom_rows
  # We artificially lower the instr_num compared to its limits, because higher
  # values can lead to register spills..
  max_num = 1 << (total_num.bit_length() - 1)  # power of 2 <= than total_num
  max_num = min(max_num, 32 // regs_per_instr)
  for lane_step in range(num_row_steps):
    addr_row = arith.addi(base_addr, utils.c((lane_step * atom_rows) << 16, i32))
    num_processed = 0
    instr_num = max_num
    while (remaining := total_num - num_processed) > 0:
      while instr_num > remaining:
        instr_num //= 2
      num_slice = slice(num_processed, num_processed + instr_num)
      addr_row_col = arith.addi(
          addr_row, utils.c(num_processed * atom_cols // tmem_packing, i32)
      )
      yield addr_row_col, instr_num, lane_step, num_slice
      num_processed += instr_num
    assert num_processed == total_num

