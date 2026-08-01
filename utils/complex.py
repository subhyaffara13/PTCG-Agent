
def complex(real: TensorLikeType, imag: TensorLikeType) -> TensorLikeType:
    allowed_dtypes = (torch.float32, torch.float64, torch.float16)
    torch._check(
        real.dtype in allowed_dtypes and imag.dtype in allowed_dtypes,
        lambda: (
            f"Expected both inputs to be Half, Float or Double tensors but got "
            f"{real.dtype} and {imag.dtype}"
        ),
    )
    torch._check(
        real.dtype == imag.dtype,
        lambda: (
            f"Expected object of scalar type {real.dtype} but got "
            f"scalar type {imag.dtype} for second argument"
        ),
    )
    result_dtype = utils.corresponding_complex_dtype(real.dtype)  # type: ignore[arg-type]
    common_shape = _broadcast_shapes(real.shape, imag.shape)
    result = real.new_empty(
        common_shape,
        dtype=result_dtype,
        layout=real.layout,
        device=real.device,
        # pin_memory=real.is_pinned(),  # NYI
    )
    result.real = real
    result.imag = imag
    return result


def complex(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ComplexOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def complex(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ComplexOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def complex(type):
    return ComplexType.get(type)


def complex(x, y):
  return x + np.complex64(1j) * y


def complex(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise make complex number: :math:`x + jy`.

  This function lowers directly to the `stablehlo.complex`_ operation.

  Args:
    x, y: input arrays. Must have matching floating-point dtypes. If
      neither is a scalar, the two arrays must have the same number
      of dimensions and be broadcast-compatible.

  Returns:
    The complex array with the real part given by ``x``, and the imaginary
    part given by ``y``. For inputs of dtype float32 or float64, the result
    will have dtype complex64 or complex128 respectively.

  See also:
    - :func:`jax.lax.real`: elementwise extract real part.
    - :func:`jax.lax.imag`: elementwise extract imaginary part.
    - :func:`jax.lax.conj`: elementwise complex conjugate.

  .. _stablehlo.complex: https://openxla.org/stablehlo/spec#complex
  """
  x, y = core.auto_insert_reshard(x, y)
  return complex_p.bind(x, y)

