
def add(
    image1: Image.Image, image2: Image.Image, scale: float = 1.0, offset: float = 0
) -> Image.Image:
    """
    Adds two images, dividing the result by scale and adding the
    offset. If omitted, scale defaults to 1.0, and offset to 0.0. ::

        out = ((image1 + image2) / scale + offset)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_add(image2.im, scale, offset))


def add(m1: torch.Tensor, m2: torch.Tensor, inplace: bool) -> torch.Tensor:
    # The first operation in a checkpoint can't be in-place, but it's
    # nice to have in-place addition during inference. Thus...
    if not inplace:
        m1 = m1 + m2
    else:
        m1 += m2

    return m1


def add(import_name: str) -> None:
    if isinstance(import_name, types.ModuleType):
        return add(import_name.__name__)
    assert isinstance(import_name, str)
    from importlib.util import find_spec

    module_spec = find_spec(import_name)
    if not module_spec:
        return
    origin = module_spec.origin
    if origin is None:
        return
    SKIP_DIRS.append(_strip_init_py(origin))
    _recompile_re()


def add(
    x: torch.Tensor,
    y: torch.Tensor,
    *,
    alpha: torch.types.Number | None = None,
) -> torch.Tensor:
    # Require both x and y to be complex tensors.
    x_is_complex_tensor = torch.is_tensor(x) and x.is_complex()
    y_is_complex_tensor = torch.is_tensor(y) and y.is_complex()
    if not x_is_complex_tensor or not y_is_complex_tensor:
        return NotImplemented

    def _requires_fallback(tensor: torch.Tensor) -> bool:
        if tensor.ndim == 0:
            return False
        # Viewing complex tensors as their real dtype requires the last stride to be 1.
        return tensor.stride()[-1] != 1

    output_size_zero = False
    if x.ndim == 0 and y.ndim == 0:
        output_size_zero = True

    if x.ndim == 0:
        x = x.reshape(1)
    if y.ndim == 0:
        y = y.reshape(1)

    z = y
    if alpha is not None:
        z = alpha * y
    complex_type = torch.promote_types(x.dtype, y.dtype)

    if _requires_fallback(x) or _requires_fallback(z):
        return NotImplemented

    # For complex typed `x`, `x.view(x.real.dtype)` doubles the last dimension and can cause problem
    # when broadcasting the add.
    def reshape_tensor_complex(tensor: torch.Tensor) -> torch.Tensor:
        """Reshape tensor from [*initial_dims, last_dim] to *initial_dims, last_dim/2, 2]"""
        # Get the current shape of the tensor
        *initial_dims, last_dim = tensor.shape

        # Check if the last dimension is even. We should never reach here since `x.view(x.real.dtype)`
        # doubles the last dimension for complex numbers.
        if last_dim % 2 != 0:
            raise AssertionError(
                "The size of the last dimension must be even to reshape it to [..., last_dim/2, 2]"
            )

        # Reshape the tensor
        new_shape = (*initial_dims, last_dim // 2, 2)
        reshaped_tensor = tensor.view(new_shape)
        return reshaped_tensor

    # Manually resolve complex tensors, as .is_conj() is unreliable after cloning during compilation.
    x = x + 0
    z = z + 0

    x_reshaped = reshape_tensor_complex(x.view(x.real.dtype))
    z_reshaped = reshape_tensor_complex(z.view(y.real.dtype))
    result = torch.flatten(x_reshaped + z_reshaped, start_dim=-2).view(complex_type)

    if output_size_zero:
        return result[0]
    return result


def add(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
    *,
    alpha: NumberType | None = None,
):
    """
    Reference implementation of torch.add
    """

    a, b = _maybe_broadcast(a, b)

    if alpha is not None:
        dtype = _binary_op_dtype(a, b)
        python_type = utils.dtype_to_type(dtype)
        if python_type is not bool and not utils.is_weakly_lesser_type(
            type(alpha), python_type
        ):
            msg = f"alpha argument of type {type(alpha)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        if isinstance(b, TensorLike):
            b = prims.mul(b, alpha)
        else:
            b = b * alpha

    output = prims.add(a, b)
    return handle_noncontiguous_outputs([a, b], output)


def add(g: jit_utils.GraphContext, self, other, alpha=None):
    if symbolic_helper._is_value(self) and symbolic_helper._is_tensor_list(self):
        tensor_list_node = other.node()
        if tensor_list_node.kind() != "prim::ListConstruct":
            return symbolic_helper._unimplemented(
                "add", "does not support adding dynamic tensor list to another"
            )
        tensors = symbolic_helper._unpack_list(other)
        l = self
        for t in tensors:
            l = g.op("SequenceInsert", l, t)
        return l

    return opset9.add(g, self, other, alpha)


def add(g: jit_utils.GraphContext, self, other, alpha=None):
    """
    This function takes the add function and returns the corresponding ONNX operator.

    This function is not meant to be called directly by the user.

    Args:
        g (GraphContext): The graph context.
        self (Tensor): The first operand.
        other (Tensor): The second operand.
        alpha (float, optional): The scaling factor for the second operand. Defaults to None.

    Returns:
        ONNX operator.
    """
    if symbolic_helper._is_value(self) and symbolic_helper._is_tensor_list(self):
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "Add", 9, 11, "Add between list of tensors not supported", self
        )
    if alpha and symbolic_helper._scalar(symbolic_helper._maybe_get_scalar(alpha)) != 1:
        other = g.op("Mul", other, alpha)
    return g.op("Add", self, other)


def add(*args):
    return sum(args)


def add(lhs: _ods_ir.Value, rhs: _ods_ir.Value, overflow_flags, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AddOp(lhs=lhs, rhs=rhs, overflowFlags=overflow_flags, results=results, loc=loc, ip=ip).result


def add(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return AddOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def add(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return AddOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def add(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise addition: :math:`x + y`.

  This function lowers directly to the `stablehlo.add`_ operation.

  Args:
    x, y: Input arrays. Must have matching numerical dtypes. If neither
      is a scalar, ``x`` and ``y`` must have the same number of dimensions
      and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the sum
    of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.add`: NumPy-style addition supporting inputs
      with mixed dtypes and ranks.

  .. _stablehlo.add: https://openxla.org/stablehlo/spec#add
  """
  x, y = core.auto_insert_reshard(x, y)
  return add_p.bind(x, y)


def add(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Add two arrays element-wise.

  JAX implementation of :obj:`numpy.add`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``+`` operator for
  JAX arrays.

  Args:
    x, y: arrays to add. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise addition.

  Examples:
    Calling ``add`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.add(x, 10)
    Array([10, 11, 12, 13], dtype=int32)

    Calling ``add`` via the ``+`` operator:

    >>> x + 10
    Array([10, 11, 12, 13], dtype=int32)
  """
  x, y = promote_args("add", x, y)
  if x.dtype == bool:
    return lax.bitwise_or(x, y)
  out = lax.add(x, y)
  jnp_error._set_error_if_nan(out)
  return out


def add(x,y):
  return x+y


def add(x,y):
  return x+y


def add(x,y):
  return x+y

