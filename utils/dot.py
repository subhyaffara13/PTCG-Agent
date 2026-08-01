
def dot(self: list[int], tensor: list[int]):
    if not (len(self) == 1 and len(tensor) == 1):
        raise AssertionError(
            f"Expected 1D tensors for dot, got len(self)={len(self)}, "
            f"len(tensor)={len(tensor)}"
        )
    if self[0] != tensor[0]:
        raise AssertionError(
            f"Dot product dimension mismatch: self[0]={self[0]}, tensor[0]={tensor[0]}"
        )
    out: list[int] = []
    return out


def dot(a: ArrayLike, b: ArrayLike, out: OutArray | None = None):
    dtype = _dtypes_impl.result_type_impl(a, b)
    is_bool = dtype == torch.bool
    if is_bool:
        dtype = torch.uint8

    a = _util.cast_if_needed(a, dtype)
    b = _util.cast_if_needed(b, dtype)

    if a.ndim == 0 or b.ndim == 0:
        result = a * b
    else:
        result = torch.matmul(a, b)

    if is_bool:
        result = result.to(torch.bool)

    return result


def dot(self, other):
    if self.is_complex():
        if self.is_conj():
            if other.is_conj():
                return torch.dot(self.conj(), other.conj()).conj()
            else:
                return torch.vdot(self.conj(), other)
        elif other.is_conj():
            return torch.vdot(other.conj(), self)

    return (self * other).sum()


def dot(g: jit_utils.GraphContext, self, other):
    return matmul(g, self, other)


def dot(vect1, vect2):
    """
    Returns dot product of two vectors.

    Examples
    ========

    >>> from sympy.vector import CoordSys3D
    >>> from sympy.vector.vector import dot
    >>> R = CoordSys3D('R')
    >>> v1 = R.i + R.j + R.k
    >>> v2 = R.x * R.i + R.y * R.j + R.z * R.k
    >>> dot(v1, v2)
    R.x + R.y + R.z

    """
    if isinstance(vect1, Add):
        return Add.fromiter(dot(i, vect2) for i in vect1.args)
    if isinstance(vect2, Add):
        return Add.fromiter(dot(vect1, i) for i in vect2.args)
    if isinstance(vect1, BaseVector) and isinstance(vect2, BaseVector):
        if vect1._sys == vect2._sys:
            return S.One if vect1 == vect2 else S.Zero
        from .functions import express
        try:
            v = express(vect2, vect1._sys)
        except ValueError:
            return Dot(vect1, vect2)
        else:
            return dot(vect1, v)
    if isinstance(vect1, VectorZero) or isinstance(vect2, VectorZero):
        return S.Zero
    if isinstance(vect1, VectorMul):
        v1, m1 = next(iter(vect1.components.items()))
        return m1*dot(v1, vect2)
    if isinstance(vect2, VectorMul):
        v2, m2 = next(iter(vect2.components.items()))
        return m2*dot(vect1, v2)

    return Dot(vect1, vect2)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def dot(vec1, vec2):
    """Dot product convenience wrapper for Vector.dot(): \n"""
    if not isinstance(vec1, (Vector, Dyadic)):
        raise TypeError('Dot product is between two vectors')
    return vec1 & vec2


def dot(a, b, strict=False, out=None):
    """
    Return the dot product of two arrays.

    This function is the equivalent of `numpy.dot` that takes masked values
    into account. Note that `strict` and `out` are in different position
    than in the method version. In order to maintain compatibility with the
    corresponding method, it is recommended that the optional arguments be
    treated as keyword only.  At some point that may be mandatory.

    Parameters
    ----------
    a, b : masked_array_like
        Inputs arrays.
    strict : bool, optional
        Whether masked data are propagated (True) or set to 0 (False) for
        the computation. Default is False.  Propagating the mask means that
        if a masked value appears in a row or column, the whole row or
        column is considered masked.
    out : masked_array, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a,b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

    See Also
    --------
    numpy.dot : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.array([[1, 2, 3], [4, 5, 6]], mask=[[1, 0, 0], [0, 0, 0]])
    >>> b = np.ma.array([[1, 2], [3, 4], [5, 6]], mask=[[1, 0], [0, 0], [0, 0]])
    >>> np.ma.dot(a, b)
    masked_array(
      data=[[21, 26],
            [45, 64]],
      mask=[[False, False],
            [False, False]],
      fill_value=999999)
    >>> np.ma.dot(a, b, strict=True)
    masked_array(
      data=[[--, --],
            [--, 64]],
      mask=[[ True,  True],
            [ True, False]],
      fill_value=999999)

    """
    if strict is True:
        if np.ndim(a) == 0 or np.ndim(b) == 0:
            pass
        elif b.ndim == 1:
            a = _mask_propagate(a, a.ndim - 1)
            b = _mask_propagate(b, b.ndim - 1)
        else:
            a = _mask_propagate(a, a.ndim - 1)
            b = _mask_propagate(b, b.ndim - 2)
    am = ~getmaskarray(a)
    bm = ~getmaskarray(b)

    if out is None:
        d = np.dot(filled(a, 0), filled(b, 0))
        m = ~np.dot(am, bm)
        if np.ndim(d) == 0:
            d = np.asarray(d)
        r = d.view(get_masked_subclass(a, b))
        r.__setmask__(m)
        return r
    else:
        d = np.dot(filled(a, 0), filled(b, 0), out._data)
        if out.mask.shape != d.shape:
            out._mask = np.empty(d.shape, MaskType)
        np.dot(am, bm, out._mask)
        np.logical_not(out._mask, out._mask)
        return out


def dot(a, b, out=None):
    """
    dot(a, b, out=None)

    Dot product of two arrays. Specifically,

    - If both `a` and `b` are 1-D arrays, it is inner product of vectors
      (without complex conjugation).

    - If both `a` and `b` are 2-D arrays, it is matrix multiplication,
      but using :func:`matmul` or ``a @ b`` is preferred.

    - If either `a` or `b` is 0-D (scalar), it is equivalent to
      :func:`multiply` and using ``numpy.multiply(a, b)`` or ``a * b`` is
      preferred.

    - If `a` is an N-D array and `b` is a 1-D array, it is a sum product over
      the last axis of `a` and `b`.

    - If `a` is an N-D array and `b` is an M-D array (where ``M>=2``), it is a
      sum product over the last axis of `a` and the second-to-last axis of
      `b`::

        dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])

    It uses an optimized BLAS library when possible (see `numpy.linalg`).

    Parameters
    ----------
    a : array_like
        First argument.
    b : array_like
        Second argument.
    out : ndarray, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a,b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

    Returns
    -------
    output : ndarray
        Returns the dot product of `a` and `b`.  If `a` and `b` are both
        scalars or both 1-D arrays then a scalar is returned; otherwise
        an array is returned.
        If `out` is given, then it is returned.

    Raises
    ------
    ValueError
        If the last dimension of `a` is not the same size as
        the second-to-last dimension of `b`.

    See Also
    --------
    vdot : Complex-conjugating dot product.
    vecdot : Vector dot product of two arrays.
    tensordot : Sum products over arbitrary axes.
    einsum : Einstein summation convention.
    matmul : '@' operator as method with out parameter.
    linalg.multi_dot : Chained dot product.

    Examples
    --------
    >>> import numpy as np
    >>> np.dot(3, 4)
    12

    Neither argument is complex-conjugated:

    >>> np.dot([2j, 3j], [2j, 3j])
    (-13+0j)

    For 2-D arrays it is the matrix product:

    >>> a = [[1, 0], [0, 1]]
    >>> b = [[4, 1], [2, 2]]
    >>> np.dot(a, b)
    array([[4, 1],
           [2, 2]])

    >>> a = np.arange(3*4*5*6).reshape((3,4,5,6))
    >>> b = np.arange(3*4*5*6)[::-1].reshape((5,4,6,3))
    >>> np.dot(a, b)[2,3,2,1,2,2]
    499128
    >>> sum(a[2,3,2,:] * b[1,2,:,2])
    499128

    """
    return (a, b, out)


def dot(a: _ods_ir.Value[_ods_ir.RankedTensorType], b: _ods_ir.Value[_ods_ir.RankedTensorType], c: _ods_ir.Value[_ods_ir.RankedTensorType], *, input_precision: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, max_num_imprecise_acc: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DotOp(a=a, b=b, c=c, inputPrecision=input_precision, maxNumImpreciseAcc=max_num_imprecise_acc, results=results, loc=loc, ip=ip).result


def dot(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DotOp(result=result, lhs=lhs, rhs=rhs, precision_config=precision_config, loc=loc, ip=ip).result


def dot(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DotOp(result=result, lhs=lhs, rhs=rhs, precision_config=precision_config, loc=loc, ip=ip).result


def dot(lhs: ArrayLike, rhs: ArrayLike, *,
        dimension_numbers: DotDimensionNumbers | None = None,
        precision: PrecisionLike = None,
        preferred_element_type: DTypeLike | None = None,
        out_sharding=None) -> Array:
  """General dot product/contraction operator.

  This operation lowers directly to the `stablehlo.dot_general`_ operation.

  The semantics of ``dot_general`` are complicated, but most users should not have to
  use it directly. Instead, you can use higher-level functions like :func:`jax.numpy.dot`,
  :func:`jax.numpy.matmul`, :func:`jax.numpy.tensordot`, :func:`jax.numpy.einsum`,
  and others which will construct appropriate calls to ``dot_general`` under the hood.
  If you really want to understand ``dot_general`` itself, we recommend reading XLA's
  DotGeneral_ operator documentation.

  Args:
    lhs: an array
    rhs: an array
    dimension_numbers: an optional tuple of tuples of sequences of ints of the form
      ``((lhs_contracting_dims, rhs_contracting_dims), (lhs_batch_dims,
      rhs_batch_dims))``. This may be left unspecified in the common case of
      un-batched matrix-matrix, matrix-vector, or vector-vector dot products, as
      determined by the shape of ``lhs`` and ``rhs``.
    precision: Optional. This parameter controls the numerics of the
      computation, and it can be one of the following:

      - ``None``, which means the default precision for the current backend,
      - a :class:`~jax.lax.Precision` enum value or a tuple of two
        :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and
        ``rhs``, or
      - a :class:`~jax.lax.DotAlgorithm` or a
        :class:`~jax.lax.DotAlgorithmPreset` indicating the algorithm that
        must be used to accumulate the dot product.

    preferred_element_type: Optional. This parameter controls the data type
      output by the dot product. By default, the output element type of this
      operation will match the ``lhs`` and ``rhs`` input element types under
      the usual type promotion rules. Setting ``preferred_element_type`` to a
      specific ``dtype`` will mean that the operation returns that element type.
      When ``precision`` is not a :class:`~jax.lax.DotAlgorithm` or
      :class:`~jax.lax.DotAlgorithmPreset`, ``preferred_element_type`` provides
      a hint to the compiler to accumulate the dot product using this data type.
    out_sharding: an optional sharding specification for the output. If not specified,
      it will be determined automatically by the compiler.

  Returns:
    An array whose first dimensions are the (shared) batch dimensions, followed
    by the ``lhs`` non-contracting/non-batch dimensions, and finally the ``rhs``
    non-contracting/non-batch dimensions.

  .. _stablehlo.dot_general: https://openxla.org/stablehlo/spec#dot_general
  .. _DotGeneral: https://www.openxla.org/xla/operation_semantics#dotgeneral
  """
  lhs_shape = np.shape(lhs)
  lhs_ndim = len(lhs_shape)

  rhs_shape = np.shape(rhs)
  rhs_ndim = len(rhs_shape)

  if dimension_numbers is None:
    if 1 <= lhs_ndim <= 2 and 1 <= rhs_ndim <= 2 and core.definitely_equal(lhs_shape[-1], rhs_shape[0]):
      dimension_numbers = (((lhs_ndim - 1,), (0,)), ((), ()))
    else:
      raise ValueError(
        "jax.lax.dot: dimension_numbers must be specified when not performing simple"
        " un-batched matrix-matrix, matrix-vector, or vector-vector products;"
        f" got {lhs_shape=} {rhs_shape=}")

  out_sharding = canonicalize_sharding(out_sharding, 'dot_general')
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  preferred_element_type = (
      None if preferred_element_type is None else
      dtypes.check_and_canonicalize_user_dtype(preferred_element_type, 'dot'))
  lhs, rhs = core.auto_insert_reshard(lhs, rhs)
  return dot_general_p.bind(lhs, rhs,
                            dimension_numbers=(cdims, bdims),
                            precision=canonicalize_precision(precision),
                            preferred_element_type=preferred_element_type,
                            out_sharding=out_sharding)


def dot(a: ArrayLike, b: ArrayLike, *,
        precision: lax.PrecisionLike = None,
        preferred_element_type: DTypeLike | None = None,
        out_sharding=None) -> Array:
  """Compute the dot product of two arrays.

  JAX implementation of :func:`numpy.dot`.

  This differs from :func:`jax.numpy.matmul` in two respects:

  - if either ``a`` or ``b`` is a scalar, the result of ``dot`` is equivalent to
    :func:`jax.numpy.multiply`, while the result of ``matmul`` is an error.
  - if ``a`` and ``b`` have more than 2 dimensions, the batch indices are
    stacked rather than broadcast.

  Args:
    a: first input array, of shape ``(*a_batch, N)``.
    b: second input array. Must have shape ``(N,)`` or ``(*b_batch, N, M)``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    An array containing the dot product of the inputs.  Unlike :func:`matmul`,
    the batch dimensions of ``a`` and ``b`` are stacked rather than broadcast;
    that is, the output shape will be ``(*a_batch,)`` if ``b`` is one-dimensional,
    or ``(*a_batch, *b_batch, M)`` if ``b`` has more than one dimension.

  See also:
    - :func:`jax.numpy.matmul`: broadcasted batched matmul.
    - :func:`jax.lax.dot_general`: general batched matrix multiplication.

  Examples:
    For scalar inputs, ``dot`` computes the element-wise product:

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.dot(x, 2)
    Array([2, 4, 6], dtype=int32)

    For vector or matrix inputs, ``dot`` computes the vector or matrix product:

    >>> M = jnp.array([[2, 3, 4],
    ...                [5, 6, 7],
    ...                [8, 9, 0]])
    >>> jnp.dot(M, x)
    Array([20, 38, 26], dtype=int32)
    >>> jnp.dot(M, M)
    Array([[ 51,  60,  29],
           [ 96, 114,  62],
           [ 61,  78,  95]], dtype=int32)

    For higher-dimensional matrix products, batch dimensions are stacked, whereas
    in :func:`~jax.numpy.matmul` they are broadcast. For example:

    >>> a = jnp.zeros((3, 2, 4))
    >>> b = jnp.zeros((3, 4, 1))
    >>> jnp.dot(a, b).shape
    (3, 2, 3, 1)
    >>> jnp.matmul(a, b).shape
    (3, 2, 1)
  """
  a, b = util.ensure_arraylike("dot", a, b)
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(
        a, b, return_weak_type_flag=True)
  else:
    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, "dot")
    output_weak_type = False

  batch_dims = ((), ())
  a_ndim, b_ndim = np.ndim(a), np.ndim(b)
  if a_ndim == 0 or b_ndim == 0:
    contract_dims: tuple[tuple[int, ...], tuple[int, ...]] = ((), ())
  else:
    if b_ndim == 1:
      contract_dims = ((a_ndim - 1,), (0,))
    else:
      contract_dims = ((a_ndim - 1,), (b_ndim - 2,))
  result = lax.dot_general(a, b, dimension_numbers=(contract_dims, batch_dims),
                           precision=precision,
                           preferred_element_type=preferred_element_type,
                           out_sharding=out_sharding)
  return lax._convert_element_type(result, preferred_element_type,
                                   output_weak_type)


def dot(a, b, trans_a: bool = False, trans_b: bool = False,
        allow_tf32: bool | None = None, precision=None):
  """Computes the dot product of two arrays.

  The inputs can optionally be transposed before computing the
  product. Depending on the hardware, this can be cheaper than
  computing the transpose beforehand.

  Args:
    a: The left-hand size of the dot product, of shape ``(..., N)``.
    b: The right-hand size of the dot product, of shape ``(...N, M)``.
    trans_a: Whether to transpose ``a`` before the product.
    trans_b: Whether to transpose ``b`` before the product.
    allow_tf32: Whether to use tf32 precision.
      Mutually exclusive with ``precision``.
    precision: Specifies the precision of the dot product.

  See Also:
    :func:`jax.numpy.dot`
  """
  if (a.ndim != 2) or (b.ndim != 2):
    raise ValueError("`a` and `b` must be 2D arrays.")
  lhs_contract_dim = 0 if trans_a else 1
  rhs_contract_dim = 0 if not trans_b else 1
  if allow_tf32 is not None:
    if precision is not None:
      raise ValueError("Only one of allow_tf32 and precision can be specified")
    precision = lax.Precision.HIGH if allow_tf32 else lax.Precision.HIGHEST

  dtype = jnp.promote_types(_handle_small(a.dtype), _handle_small(b.dtype))
  if jnp.issubdtype(dtype, jnp.integer):
    out_dtype = jnp.int32
  elif dtype == jnp.float64:
    out_dtype = jnp.float64
  else:
    out_dtype = jnp.float32
  return lax.dot_general(
      a,
      b,
      dimension_numbers=(((lhs_contract_dim,), (rhs_contract_dim,)), ((), ())),
      precision=precision,
      preferred_element_type=out_dtype,
  )


def dot(lhs: Any, rhs: Any, sum_dims: Any) -> _Tensor | torch.Tensor:
    """
    Perform dot product between two tensors along specified dimensions.

    Args:
        lhs: Left-hand side tensor
        rhs: Right-hand side tensor
        sum_dims: Dimensions to sum over (contract)

    Returns:
        Result of dot product
    """
    # Get tensor info
    lhs_info = TensorInfo.create(lhs, ensure_batched=False, ensure_present=False)
    rhs_info = TensorInfo.create(rhs, ensure_batched=False, ensure_present=False)

    if not (lhs_info and rhs_info):
        # Fall back to regular operations
        return torch.matmul(lhs, rhs)

    if lhs_info.tensor is None or rhs_info.tensor is None:
        raise AssertionError("Cannot perform dot product on None tensors")

    lhs_strides = lhs_info.tensor.stride()
    rhs_strides = rhs_info.tensor.stride()

    # Create dot parts for different dimension categories
    lro_dims = DotPart()  # Left-right-output (batch dims)
    lo_dims = DotPart()  # Left-output only
    ro_dims = DotPart()  # Right-output only
    lr_dims = DotPart()  # Left-right (contracted dims)

    def insert_dim(d: Any, lhs_idx: Any, rhs_idx: Any) -> None:
        """Insert dimension into appropriate part based on stride pattern."""
        reduced = d in sum_dims
        lhs_stride = lhs_strides[lhs_idx] if lhs_idx is not None else 0
        rhs_stride = rhs_strides[rhs_idx] if rhs_idx is not None else 0

        if reduced:
            lr_dims.append(d)
        else:
            if (lhs_stride == 0) == (rhs_stride == 0):
                lro_dims.append(d)  # Both have or both lack this dim
            elif lhs_stride != 0:
                lo_dims.append(d)  # Only lhs has this dim
            else:
                ro_dims.append(d)  # Only rhs has this dim

    # Track which rhs dimensions we've seen
    rhs_seen = [False] * len(rhs_info.levels)

    # Process lhs dimensions
    for i, lhs_level in enumerate(lhs_info.levels):
        rhs_idx = None
        for j, rhs_level in enumerate(rhs_info.levels):
            if lhs_level == rhs_level:
                rhs_idx = j
                rhs_seen[j] = True
                break

        insert_dim(lhs_level, i, rhs_idx)

    # Process remaining rhs dimensions
    for i, rhs_level in enumerate(rhs_info.levels):
        if not rhs_seen[i]:
            insert_dim(rhs_level, None, i)

    # Validate sum dimensions exist
    if len(lr_dims.dims) != len(sum_dims):
        for d in sum_dims:
            if d not in lhs_info.levels and d not in rhs_info.levels:
                raise ValueError(f"summing over non-existent dimension {d}")

    # Prepare tensors and perform matrix multiplication
    if len(lro_dims.dims) != 0:
        # Batched matrix multiply
        lhs_tensor = dot_prepare([lro_dims, lo_dims, lr_dims], lhs_info)
        rhs_tensor = dot_prepare([lro_dims, lr_dims, ro_dims], rhs_info)
        result = torch.bmm(lhs_tensor, rhs_tensor)
        return dot_finish([lro_dims, lo_dims, ro_dims], result)
    else:
        # Regular matrix multiply
        lhs_tensor = dot_prepare([lo_dims, lr_dims], lhs_info)
        rhs_tensor = dot_prepare([lr_dims, ro_dims], rhs_info)
        result = torch.mm(lhs_tensor, rhs_tensor)
        return dot_finish([lo_dims, ro_dims], result)


def dot(v1, v2):
    """Return the dot product of two vectors.

    Args:
        v1 (complex): First vector.
        v2 (complex): Second vector.

    Returns:
        double: Dot product.
    """
    result = (v1 * v2.conjugate()).real
    # When vectors are perpendicular (i.e. dot product is 0), the above expression may
    # yield slightly different results when running in pure Python vs C/Cython,
    # both of which are correct within IEEE-754 floating-point precision.
    # It's probably due to the different order of operations and roundings in each
    # implementation. Because we are using the result in a denominator and catching
    # ZeroDivisionError (see `calc_intersect`), it's best to normalize the result here.
    if abs(result) < 1e-15:
        result = 0.0
    return result

