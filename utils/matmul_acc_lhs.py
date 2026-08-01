
def matmul_acc_lhs(acc: _Union[int, _ods_ir.IntegerAttr], lhs: _ods_ir.Value[_ods_ir.VectorType], mxu_index: _Union[int, _ods_ir.IntegerAttr], *, load_staged_rhs: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MatmulAccLhsOp:
  return MatmulAccLhsOp(acc=acc, lhs=lhs, mxu_index=mxu_index, load_staged_rhs=load_staged_rhs, loc=loc, ip=ip)


def matmul_acc_lhs(
    acc_addr: int,
    lhs: jax.Array,
    mxu_index: int,
    load_staged_rhs: int | None = None,
) -> None:
  """Performs a matrix multiplication in the chosen MXU.

  If `load_staged_rhs` is not None, the previously pushed RHS will be loaded
  from the given staging register _before_ the matrix multiplication begins.
  The results of the multiplication are accumulated into the specified
  accumulator slice.

  Args:
    acc_addr: The base address of the accumulator slice used for results.
    lhs: The left-hand side operand. Must be M x 256. For M divisible by the
      number of sublanes multiplied by datatype packing.
    mxu_index: The MXU to use.
    load_staged_rhs: The staging register to load the RHS from. If None, the RHS
      is not loaded from staging and the matmul will reuse the existing one.
  """
  # This is a common error. You might intend to say to load the staged RHS, but
  # True is equivalent to saying "load the staged RHS FROM REGISTER 1", which is
  # probably not what you intended.
  if isinstance(load_staged_rhs, bool):
    raise TypeError("load_staged_rhs must be an integer or None.")
  matmul_acc_lhs_p.bind(
      lhs,
      acc_addr=acc_addr,
      mxu_index=mxu_index,
      load_staged_rhs=load_staged_rhs,
  )

