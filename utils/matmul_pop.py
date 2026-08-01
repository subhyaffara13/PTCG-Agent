
def matmul_pop(result: _ods_ir.Type, acc: _Union[int, _ods_ir.IntegerAttr], mxu_index: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MatmulPopOp(result=result, acc=acc, mxu_index=mxu_index, loc=loc, ip=ip).result


def matmul_pop(
    acc_addr: int,
    shape: tuple[int, int],
    dtype: jax.typing.DTypeLike,
    mxu_index: int,
):
  """Returns the result of a matrix multiplication from the chosen MXU and zeroes the accumulator.

  If the result is not ready yet (the MXU is still busy), the operation blocks.

  ```{warning}
  The kernel must not leave any data in the accumulator upon exit.
  ```

  Args:
    acc_addr: The base address of the popped accumulator slice.
    shape: The shape of the result.
    dtype: The dtype of the result.
    mxu_index: The MXU to use.
  """
  return matmul_pop_p.bind(
      acc_addr=acc_addr,
      shape=shape,
      mxu_index=mxu_index,
      dtype=jnp.dtype(dtype),
  )

