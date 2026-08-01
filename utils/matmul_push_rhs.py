
def matmul_push_rhs(rhs: _ods_ir.Value[_ods_ir.VectorType], mxu_index: _Union[int, _ods_ir.IntegerAttr], *, staging_register: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, transpose: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MatmulPushRhsOp:
  return MatmulPushRhsOp(rhs=rhs, mxu_index=mxu_index, staging_register=staging_register, transpose=transpose, loc=loc, ip=ip)


def matmul_push_rhs(
    rhs: jax.Array,
    staging_register: int,
    mxu_index: int,
    *,
    transpose: bool = False,
) -> None:
  """Prepares the RHS for a matrix multiplication in the chosen MXU.

  Each MXU has an independent set of staging registers.

  ```{warning}
  It is not allowed to push to the same staging register twice. Once
  the RHS is prepared, it must be loaded into the MXU using `matmul_acc_lhs`
  before it can be used again.
  ```

  ```{warning}
  The kernel must not leave any data in the staging registers upon exit.
  ```

  Args:
    rhs: The right-hand side operand. Must be 256x256.
    staging_register: The staging register to use.
    mxu_index: The MXU to use.
    transpose: Whether to transpose the RHS.
  """
  matmul_push_rhs_p.bind(
      rhs,
      staging_register=staging_register,
      mxu_index=mxu_index,
      transpose=transpose,
  )

