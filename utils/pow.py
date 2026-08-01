
def pow(a, b):
    if isinstance(b, float) and b.is_integer():
        return pow(a, int(b))
    elif isinstance(b, float) and b == 0.5:
        return sqrt(a)
    elif isinstance(b, int) and b == 1:
        return clone(a)

    # Type promotion ensures all tensor arguments have the same type
    dtype = next(x.get_dtype() for x in (a, b) if isinstance(x, ir.TensorBox))
    is_integer_pow = is_integer_dtype(dtype)

    # Optimize away small fixed powers, or for integers avoid falling back to ATen
    embed_exponent = isinstance(b, int) and (
        -32 < b < 32 or (is_integer_pow and b >= 0)
    )
    if embed_exponent:
        loader = a.make_loader()

        def fn(idx):
            return pow_recursive(loader(idx), b, a.get_dtype())

        return Pointwise.create(
            device=a.get_device(),
            dtype=a.get_dtype(),
            inner_fn=fn,
            ranges=a.get_size(),
        )

    if isinstance(a, Number):
        if a == 1:
            return full_like(b, 1)

        if a == 2 and is_float_dtype(b.get_dtype()):
            return exp2(b)

    if is_integer_pow:
        # ops.pow doesn't work for integers
        if isinstance(a, Number):
            return fallback_pow_scalar(a, b)
        elif isinstance(b, Number):
            return fallback_pow_tensor_scalar(a, b)
        else:
            return fallback_pow_tensor_tensor(a, b)

    return pow_native(a, b)


def pow(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
) -> TensorLikeType:
    if not (isinstance(a, TensorLikeType) or isinstance(b, TensorLikeType)):
        raise AssertionError("at least one of a or b must be TensorLikeType")

    if isinstance(b, Number):
        if b == 1.0:
            return a.clone()  # type: ignore[return-value,union-attr]
        elif b == 2.0:
            return a * a  # type: ignore[return-value]
        elif b == 0.5:
            return torch.sqrt(a)  # type: ignore[arg-type]
    elif isinstance(a, Number):
        if a == 1.0:
            return torch.fill(b, True)
        if a == 2.0 and (
            utils.is_float_dtype(b.dtype) or utils.is_complex_dtype(b.dtype)
        ):
            return torch.exp2(b)

    return prims.pow(a, b)


def pow(g: jit_utils.GraphContext, self, exponent):
    return g.op("Pow", self, exponent)


def pow(g: jit_utils.GraphContext, self, exponent):
    f_dtype = _type_utils.JitScalarType.from_value(self)
    if not symbolic_helper._is_fp(self):
        f_dtype = _type_utils.JitScalarType.FLOAT
        self = g.op("Cast", self, to_i=f_dtype.onnx_type())
    if not symbolic_helper._is_fp(exponent):
        exponent = g.op(
            "Cast",
            exponent,
            to_i=f_dtype.onnx_type(),
        )
    pow = g.op("Pow", self, exponent)
    return pow


def pow(matrix: Array, n: float | Array) -> Array:
    xp = array_namespace(matrix)
    device = xp_device(matrix)
    # If n is an array, we sanitize it to a scalar and promote quat and n to
    # the same dtype.
    if is_array_api_obj(n):
        if n.shape == (1,):  # type:ignore[union-attr]
            n = n[0]  # type:ignore[index]
        elif n.ndim != 0:  # type:ignore[union-attr]
            raise ValueError("Array exponent must be a scalar")
        matrix, n = xp_promote(matrix, n, force_floating=True, xp=xp)

    # If n is a lazy array, we cannot take fast paths for special cases.
    if is_lazy_array(n):
        # Lazy execution. We compute all special cases and the general case
        result = from_exp_coords(as_exp_coords(matrix) * n)
        identity = xp.eye(4, dtype=matrix.dtype, device=device)
        result = xp.where(n == 0, identity, result)
        result = xp.where(n == -1, inv(matrix), result)
        result = xp.where(n == 1, matrix, result)
        return result
    if n == 0:
        identity = xp.eye(4, dtype=matrix.dtype, device=device)
        identity = xpx.atleast_nd(identity, ndim=matrix.ndim, xp=xp)
        return xp.tile(identity, (*matrix.shape[:-2], 1, 1))
    elif n == -1:
        return inv(matrix)
    elif n == 1:
        return matrix
    return from_exp_coords(as_exp_coords(matrix) * n)


def pow(quat: Array, n: float | Array) -> Array:
    xp = array_namespace(quat)
    device = xp_device(quat)
    # If n is an array, we sanitize it to a scalar and promote quat and n to
    # the same dtype.
    if is_array_api_obj(n):
        if n.shape == (1,):  # pyrefly:ignore[missing-attribute]
            n = n[0]  # pyrefly:ignore[bad-index]
        elif n.ndim != 0:  # pyrefly:ignore[missing-attribute]
            raise ValueError("Array exponent must be a scalar")
        quat, n = xp_promote(quat, n, force_floating=True, xp=xp)

    # If n is a lazy array, we cannot take fast paths for special cases.
    if is_lazy_array(n):
        result = from_rotvec(n * as_rotvec(quat))  # general scaling of rotation angle
        # Special cases 0 -> identity, -1 -> inv, 1 -> copy
        identity = xp.zeros((*quat.shape[:-1], 4), dtype=quat.dtype, device=device)
        identity = xpx.at(identity)[..., 3].set(1)
        result = xp.where(n == 0, identity, result)
        result = xp.where(n == -1, inv(quat), result)
        result = xp.where(n == 1, quat, result)
        return result
    if n == 0:
        identity = xp.zeros((*quat.shape[:-1], 4), dtype=quat.dtype, device=device)
        return xpx.at(identity)[..., 3].set(1)
    if n == -1:
        return inv(quat)
    if n == 1:
        return quat
    return from_rotvec(n * as_rotvec(quat))


def pow(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise power: :math:`x^y`.

  This function lowers directly to the `stablehlo.pow`_ operation, along with
  a `stablehlo.convert`_ when the argument dtypes do not match.

  Args:
    x: Input array giving the base value. Must have floating or complex type.
    y: Input array giving the exponent value. Must have integer, floating, or
      complex type. Its dtype will be cast to that of ``x.dtype`` if necessary.
      If neither ``x`` nor ``y`` is a scalar, then ``x`` and ``y`` must have
      the same number of dimensions and be broadcast-compatible.

  Returns:
    An array of the same dtype as ``x`` containing the elementwise power.

  See also:
    :func:`jax.lax.integer_pow`: Elementwise power where ``y`` is a static integer.

  .. _stablehlo.convert: https://openxla.org/stablehlo/spec#convert
  .. _stablehlo.pow: https://openxla.org/stablehlo/spec#pow
  """
  x, y = core.auto_insert_reshard(x, y)
  return pow_p.bind(x, y)


def pow(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.power`"""
  return power(x1, x2)

