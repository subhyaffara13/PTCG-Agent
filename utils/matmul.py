
def matmul(A: Tensor | None, B: Tensor) -> Tensor:
    """Multiply two matrices.

    If A is None, return B. A can be sparse or dense. B is always
    dense.
    """
    if A is None:
        return B
    if is_sparse(A):
        return torch.sparse.mm(A, B)
    return torch.matmul(A, B)


def matmul(tensor1: list[int], tensor2: list[int]):
    dim_tensor1 = len(tensor1)
    dim_tensor2 = len(tensor2)
    if dim_tensor1 == 1 and dim_tensor2 == 1:
        return dot(tensor1, tensor2)
    elif dim_tensor1 == 2 and dim_tensor2 == 1:
        return mv(tensor1, tensor2)
    elif dim_tensor1 == 1 and dim_tensor2 == 2:
        return squeeze(mm(unsqueeze(tensor1, 0), tensor2), 0)
    elif dim_tensor1 == 2 and dim_tensor2 == 2:
        return mm(tensor1, tensor2)
    elif dim_tensor1 >= 1 and dim_tensor2 >= 1:
        # We are multiplying b1 x n x m1 by x2 x m2 x p (where b1 can be a list);
        # we track m1 vs m2 separately even though they must match for nicer error messages
        n = tensor1[-2] if dim_tensor1 > 1 else 1
        batch_tensor1: list[int] = []
        # TODO: handling of slice
        for i in range(dim_tensor1 - 2):
            batch_tensor1.append(tensor1[i])
        p = tensor2[-1]
        batch_tensor2: list[int] = []
        # TODO: handling of slice
        for i in range(dim_tensor2 - 2):
            batch_tensor2.append(tensor2[i])

        # expand the batch portion (i.e. cut off matrix dimensions and expand rest)
        expand_batch_portion = broadcast(batch_tensor1, batch_tensor2)

        # todo: copy ?
        output_shape = expand_batch_portion
        if dim_tensor1 > 1:
            output_shape.append(n)

        if dim_tensor2 > 1:
            output_shape.append(p)

        return output_shape
    else:
        raise AssertionError("both arguments to matmul need to be at least 1D")


def matmul(tensor1, tensor2, *, is_out=False):
    from torch.fx.experimental.symbolic_shapes import guard_or_false, guard_or_true

    dim_tensor1 = tensor1.dim()
    dim_tensor2 = tensor2.dim()
    if dim_tensor1 == 0 or dim_tensor2 == 0:
        raise AssertionError(
            f"matmul does not support 0-dimensional tensors, got dims: {dim_tensor1} and {dim_tensor2}"
        )
    if dim_tensor1 == 1 and dim_tensor2 == 1:
        return torch.dot(tensor1, tensor2)
    elif dim_tensor1 == 2 and dim_tensor2 == 1:
        return torch.mv(tensor1, tensor2)
    elif dim_tensor1 == 1 and dim_tensor2 == 2:
        return torch.squeeze(torch.mm(torch.unsqueeze(tensor1, 0), tensor2), 0)
    elif dim_tensor1 == 2 and dim_tensor2 == 2:
        return torch.mm(tensor1, tensor2)
    elif should_fold(tensor1, tensor2, is_out):
        # dim_tensor1 >=3 && (dim_tensor2 == 1 || dim_tensor2 == 2) ||
        # dim_tensor2 >=3 && (dim_tensor1 == 1 || dim_tensor1 == 2)
        # and some condition on the strides is fulfilled

        # optimization: use mm instead of bmm by folding the batch of the larger tensor
        # into its leading matrix dimension
        transpose = dim_tensor2 > dim_tensor1
        t1 = tensor2.mT if transpose else tensor1
        t2 = (
            tensor2 if not transpose else (tensor1.t() if dim_tensor1 == 2 else tensor1)
        )
        # Invariant: t1.dim() >= 3 && (t2.dim() == 1 || t2.dim() == 2)
        #            and t1 and t2 are matmul-compatible

        # Why not t1.view(-1, sizes_1[-1])?
        # If the last dim is 0, then view(-1, 0) won't work because the -1 becomes ambiguous.
        # This can happen in e.g. [3, 5, 0] @ [0, 0].
        sizes_1 = t1.shape
        output_shape = list(sizes_1[:-1])
        folded_dim1 = reduce(operator.mul, output_shape)

        # Readjust output_shape if we are multiplying by a matrix
        t2_is_matrix = t2.dim() == 2
        if t2_is_matrix:
            output_shape.append(t2.shape[1])

        # This will almost always be a view.
        # It may not be a view if t2->requires_grad(). See should_fold in aten/ for an explanation
        t1_folded = t1.reshape(folded_dim1, sizes_1[-1])
        if t2_is_matrix:
            # This copies if we perform a 2D @ 3D and the first tensor requires_grad
            # See should_fold native/LinearAlgebra.cpp for why.
            output = torch.ops.aten._unsafe_view(t1_folded.mm(t2), output_shape)
            return output.mT.contiguous() if transpose else output
        else:
            return torch.ops.aten._unsafe_view(t1_folded.mv(t2), output_shape)

    elif dim_tensor1 >= 1 and dim_tensor2 >= 1:
        # We are multiplying b1 x n x m1 by x2 x m2 x p (where b1 can be a list);
        # we track m1 vs m2 separately even though they must match for nicer error messages
        n = tensor1.size(-2) if dim_tensor1 > 1 else 1
        m1 = tensor1.size(-1)
        batch_tensor1 = tensor1.shape[:-2]
        m2 = tensor2.size(-2) if dim_tensor2 > 1 else tensor2.size(-1)
        p = tensor2.size(-1) if dim_tensor2 > 1 else 1

        batch_tensor2: list[int] = []
        # TODO: handling of slice
        for i in range(dim_tensor2 - 2):
            batch_tensor2.append(tensor2.size(i))

        # Same optimization for the gradients as that in should_fold
        # If we're going to broadcast, we force it to go through the should_fold branch
        if (
            dim_tensor1 == 3
            and dim_tensor2 == 3
            and guard_or_true(batch_tensor1[0] != batch_tensor2[0])
        ):
            if guard_or_false(batch_tensor1[0] == 1) and tensor1.requires_grad:
                return matmul(tensor1.squeeze(0), tensor2)
            if guard_or_false(batch_tensor2[0] == 1) and tensor2.requires_grad:
                return matmul(tensor1, tensor2.squeeze(0))

        # expand the batch portion (i.e. cut off matrix dimensions and expand rest)
        expand_batch_portion = list(
            torch.broadcast_shapes(batch_tensor1, batch_tensor2)
        )

        tensor1_expand_size = expand_batch_portion + [n, m1]

        expand_batch_product = prod(expand_batch_portion)

        # HACK: We need reshape with symint support
        tensor1_expanded = tensor1.expand(tensor1_expand_size).reshape(
            expand_batch_product, n, m1
        )

        vector_rhs = dim_tensor2 == 1
        if vector_rhs:
            tensor2_expand_size = expand_batch_portion + [m2]
            tensor2_expanded = (
                tensor2.expand(tensor2_expand_size)
                .reshape(expand_batch_product, m2)
                .unsqueeze(2)
            )
        else:
            tensor2_expand_size = expand_batch_portion + [m2, p]
            tensor2_expanded = tensor2.expand(tensor2_expand_size).reshape(
                expand_batch_product, m2, p
            )

        output_shape = expand_batch_portion
        if dim_tensor1 > 1:
            output_shape.append(n)

        if dim_tensor2 > 1:
            output_shape.append(p)

        if vector_rhs:
            return tensor1_expanded.bmm(tensor2_expanded).squeeze(-1).view(output_shape)
        else:
            return tensor1_expanded.bmm(tensor2_expanded).view(output_shape)
    else:
        torch._check(False, lambda: "both arguments to matmul need to be at least 1D")


def matmul(x, y):
    # work around:
    #  - RuntimeError: expected scalar type Int but found Double
    #  - RuntimeError: "addmm_impl_cpu_" not implemented for 'Bool'
    #  - RuntimeError: "addmm_impl_cpu_" not implemented for 'Half'
    dtype = _dtypes_impl.result_type_impl(x, y)
    is_bool = dtype == torch.bool
    is_half = (x.dtype == torch.float16 or y.dtype == torch.float16) and (
        x.is_cpu or y.is_cpu
    )

    work_dtype = dtype
    if is_bool:
        work_dtype = torch.uint8
    if is_half:
        work_dtype = torch.float32

    x = _util.cast_if_needed(x, work_dtype)
    y = _util.cast_if_needed(y, work_dtype)

    result = torch.matmul(x, y)

    if work_dtype != dtype:
        result = result.to(dtype)

    return result


def matmul(
    x1: ArrayLike,
    x2: ArrayLike,
    /,
    out: OutArray | None = None,
    *,
    casting: CastingModes | None = "same_kind",
    order: NotImplementedType = "K",
    dtype: DTypeLike | None = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
    axes: NotImplementedType = None,
    axis: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.result_type_impl(x1, x2)
    x1, x2 = _util.typecast_tensors((x1, x2), dtype, casting)

    result = _binary_ufuncs_impl.matmul(x1, x2)

    result = _ufunc_postprocess(result, out, casting)
    return result


def matmul(g: jit_utils.GraphContext, self, other):
    return bmm(g, self, other)


def matmul(g: jit_utils.GraphContext, self, other):
    return g.op("MatMul", self, other)


def matmul(m1, m2):
    """Multiply two matrices.

    >>> list(matmul([(7, 5), (3, 5)], [(2, 5), (7, 9)]))
    [(49, 80), (41, 60)]

    The caller should ensure that the dimensions of the input matrices are
    compatible with each other.

    Supports all numeric types: int, float, complex, Decimal, Fraction.
    """
    n = len(m2[0])
    return batched(starmap(_sumprod, product(m1, transpose(m2))), n)


def matmul(x1: Array, x2: Array, /, xp: Namespace, **kwargs: object) -> Array:
    return xp.matmul(x1, x2, **kwargs)


def matmul(x1: Array, x2: Array, /, **kwargs: object) -> Array:
    # torch.matmul doesn't type promote (but differently from _fix_promotion)
    x1, x2 = _fix_promotion(x1, x2, only_scalar=False)
    return torch.matmul(x1, x2, **kwargs)


def matmul(x1, x2, /):
    """
    Computes the matrix product.

    This function is Array API compatible, contrary to
    :func:`numpy.matmul`.

    Parameters
    ----------
    x1 : array_like
        The first input array.
    x2 : array_like
        The second input array.

    Returns
    -------
    out : ndarray
        The matrix product of the inputs.
        This is a scalar only when both ``x1``, ``x2`` are 1-d vectors.

    Raises
    ------
    ValueError
        If the last dimension of ``x1`` is not the same size as
        the second-to-last dimension of ``x2``.

        If a scalar value is passed in.

    See Also
    --------
    numpy.matmul

    Examples
    --------
    For 2-D arrays it is the matrix product:

    >>> a = np.array([[1, 0],
    ...               [0, 1]])
    >>> b = np.array([[4, 1],
    ...               [2, 2]])
    >>> np.linalg.matmul(a, b)
    array([[4, 1],
           [2, 2]])

    For 2-D mixed with 1-D, the result is the usual.

    >>> a = np.array([[1, 0],
    ...               [0, 1]])
    >>> b = np.array([1, 2])
    >>> np.linalg.matmul(a, b)
    array([1, 2])
    >>> np.linalg.matmul(b, a)
    array([1, 2])


    Broadcasting is conventional for stacks of arrays

    >>> a = np.arange(2 * 2 * 4).reshape((2, 2, 4))
    >>> b = np.arange(2 * 2 * 4).reshape((2, 4, 2))
    >>> np.linalg.matmul(a,b).shape
    (2, 2, 2)
    >>> np.linalg.matmul(a, b)[0, 1, 1]
    98
    >>> sum(a[0, 1, :] * b[0 , :, 1])
    98

    Vector, vector returns the scalar inner product, but neither argument
    is complex-conjugated:

    >>> np.linalg.matmul([2j, 3j], [2j, 3j])
    (-13+0j)

    Scalar multiplication raises an error.

    >>> np.linalg.matmul([1,2], 3)
    Traceback (most recent call last):
    ...
    ValueError: matmul: Input operand 1 does not have enough dimensions ...

    """
    return _core_matmul(x1, x2)


def matmul(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], acc: _ods_ir.Value[_ods_ir.VectorType], transpose_lhs_hint: _Union[bool, _ods_ir.BoolAttr], *, transpose_lhs: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, transpose_rhs: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, precision: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, dimension_numbers: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MatmulOp(result=result, lhs=lhs, rhs=rhs, acc=acc, transpose_lhs_hint=transpose_lhs_hint, transpose_lhs=transpose_lhs, transpose_rhs=transpose_rhs, precision=precision, dimension_numbers=dimension_numbers, loc=loc, ip=ip).result


def matmul(x1: ArrayLike, x2: ArrayLike, /, *,
           precision: lax.PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Perform a matrix multiplication.

  JAX implementation of :func:`numpy.linalg.matmul`.

  Args:
    x1: first input array, of shape ``(..., N)``.
    x2: second input array. Must have shape ``(N,)`` or ``(..., N, M)``.
      In the multi-dimensional case, leading dimensions must be broadcast-compatible
      with the leading dimensions of ``x1``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``x1`` and ``x2``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the matrix product of the inputs. Shape is ``x1.shape[:-1]``
    if ``x2.ndim == 1``, otherwise the shape is ``(..., M)``.

  See Also:
    :func:`jax.numpy.matmul`: NumPy API for this function.
    :func:`jax.numpy.linalg.vecdot`: batched vector product.
    :func:`jax.numpy.linalg.tensordot`: batched tensor product.

  Examples:
    Vector dot products:

    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.matmul(x1, x2)
    Array(32, dtype=int32)

    Matrix dot product:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> x2 = jnp.array([[1, 2],
    ...                 [3, 4],
    ...                 [5, 6]])
    >>> jnp.linalg.matmul(x1, x2)
    Array([[22, 28],
           [49, 64]], dtype=int32)

    For convenience, in all cases you can do the same computation using
    the ``@`` operator:

    >>> x1 @ x2
    Array([[22, 28],
           [49, 64]], dtype=int32)
  """
  x1, x2 = ensure_arraylike('jnp.linalg.matmul', x1, x2)
  return tensor_contractions.matmul(x1, x2, precision=precision,
                                    preferred_element_type=preferred_element_type)


def matmul(a: ArrayLike, b: ArrayLike, *,
           precision: lax.PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None,
           out_sharding: NamedSharding | P | None = None,
           ) -> Array:
  """Perform a matrix multiplication.

  JAX implementation of :func:`numpy.matmul`.

  Args:
    a: first input array, of shape ``(N,)`` or ``(..., K, N)``.
    b: second input array. Must have shape ``(N,)`` or ``(..., N, M)``.
      In the multi-dimensional case, leading dimensions must be broadcast-compatible
      with the leading dimensions of ``a``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the matrix product of the inputs. Shape is ``a.shape[:-1]``
    if ``b.ndim == 1``, otherwise the shape is ``(..., K, M)``, where leading
    dimensions of ``a`` and ``b`` are broadcast together.

  See Also:
    - :func:`jax.numpy.linalg.vecdot`: batched vector product.
    - :func:`jax.numpy.linalg.tensordot`: batched tensor product.
    - :func:`jax.lax.dot_general`: general N-dimensional batched dot product.

  Examples:
    Vector dot products:

    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.matmul(a, b)
    Array(32, dtype=int32)

    Matrix dot product:

    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> b = jnp.array([[1, 2],
    ...                [3, 4],
    ...                [5, 6]])
    >>> jnp.matmul(a, b)
    Array([[22, 28],
           [49, 64]], dtype=int32)

    For convenience, in all cases you can do the same computation using
    the ``@`` operator:

    >>> a @ b
    Array([[22, 28],
           [49, 64]], dtype=int32)
  """
  a, b = util.ensure_arraylike("matmul", a, b)
  for i, x in enumerate((a, b)):
    if np.ndim(x) < 1:
      msg = (f"matmul input operand {i} must have ndim at least 1, "
             f"but it has ndim {np.ndim(x)}")
      raise ValueError(msg)
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)
  else:
    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, "matmul")
    output_weak_type = False

  a_is_mat, b_is_mat = (np.ndim(a) > 1), (np.ndim(b) > 1)
  a_batch_dims: tuple[int | None, ...] = np.shape(a)[:-2] if a_is_mat else ()
  b_batch_dims: tuple[int | None, ...] = np.shape(b)[:-2] if b_is_mat else ()
  num_batch_dims = max(len(a_batch_dims), len(b_batch_dims))
  a_batch_dims = (None,) * (num_batch_dims - len(a_batch_dims)) + a_batch_dims
  b_batch_dims = (None,) * (num_batch_dims - len(b_batch_dims)) + b_batch_dims

  a_batch_specs = core.typeof(a).sharding.spec.partitions[:-2] if a_is_mat else ()
  b_batch_specs = core.typeof(b).sharding.spec.partitions[:-2] if b_is_mat else ()
  a_batch_specs = (None,) * (num_batch_dims - len(a_batch_specs)) + a_batch_specs
  b_batch_specs = (None,) * (num_batch_dims - len(b_batch_specs)) + b_batch_specs

  # Dimensions to squeeze from the inputs.
  a_squeeze: list[int] = []
  b_squeeze: list[int] = []
  # Dimensions squeezed from both inputs (in output dimension indices).
  both_squeeze: list[int] = []

  # Positions of batch dimensions in squeezed inputs.
  a_batch = []
  b_batch = []

  # Desired index in final output of each kind of dimension, in the order that
  # lax.dot_general will emit them.
  idx_batch: list[int] = []
  idx_a_other: list[int] = []  # other = non-batch, non-contracting.
  idx_b_other: list[int] = []
  for i, (ba, bb, sa, sb) in enumerate(zip(a_batch_dims, b_batch_dims,
                                           a_batch_specs, b_batch_specs)):
    if ba is None:
      idx_b_other.append(i)
    elif bb is None:
      idx_a_other.append(i)
    # We generate a cleaner (and more Mosaic-friendly) dot_general by
    # squeezing both and not just treating the B dim as non-contracting below.
    elif (core.definitely_equal(ba, 1) and core.definitely_equal(bb, 1)
          and sa is None and sb is None):
      a_squeeze.append(len(idx_batch) + len(idx_a_other) + len(a_squeeze))
      b_squeeze.append(len(idx_batch) + len(idx_b_other) + len(b_squeeze))
      both_squeeze.append(i)
    elif core.definitely_equal(ba, 1) and sa is None:
      idx_b_other.append(i)
      a_squeeze.append(len(idx_batch) + len(idx_a_other) + len(a_squeeze))
    elif core.definitely_equal(bb, 1) and sb is None:
      idx_a_other.append(i)
      b_squeeze.append(len(idx_batch) + len(idx_b_other) + len(b_squeeze))
    elif core.definitely_equal(ba, bb) and sa == sb:
      a_batch.append(len(idx_batch) + len(idx_a_other))
      b_batch.append(len(idx_batch) + len(idx_b_other))
      idx_batch.append(i)
    else:
      raise ValueError("Incompatible types for matmul arguments: {} and {}"
                       .format(core.typeof(a), core.typeof(b)))

  if a_is_mat:
    idx_a_other.append(num_batch_dims)
  if b_is_mat:
    idx_b_other.append(num_batch_dims + a_is_mat)
  perm = np.argsort(np.concatenate([idx_batch, idx_a_other, idx_b_other]))

  a = lax.squeeze(a, tuple(a_squeeze))
  b = lax.squeeze(b, tuple(b_squeeze))
  out = lax.dot_general(
    a, b, (((np.ndim(a) - 1,), (np.ndim(b) - 1 - b_is_mat,)), (a_batch, b_batch)),
    precision=precision, preferred_element_type=preferred_element_type,
    out_sharding=out_sharding)
  result = lax.transpose(out, perm)
  if both_squeeze:
    result = lax.expand_dims(result, tuple(both_squeeze))
  return lax._convert_element_type(result, preferred_element_type, output_weak_type)


def matmul(a, b, c, config: TuningConfig):
  dtype = a.dtype
  if a.dtype != b.dtype:
    raise ValueError(
        f"Matmul LHS and RHS have incompatible dtypes {a.dtype} vs {b.dtype}"
    )
  m, k = a.shape
  k2, n = b.shape
  assert k == k2
  if k != k2:
    raise ValueError(
        f"Matmul LHS and RHS have incompatible shapes {a.shape} vs {b.shape}"
    )
  if c is None:
    out_dtype = dtype
  else:
    if c.shape != (m, n):
      raise ValueError(f"C has incompatible shape {c.shape} vs {(m, n)}")
    out_dtype = c.dtype
  tile_m, tile_n = config.tile_m, config.tile_n
  epi_tile_n = config.epi_tile_n or tile_n
  epi_tile_m = config.epi_tile_m or tile_m
  config = dataclasses.replace(config, epi_tile_n=epi_tile_n, epi_tile_m=epi_tile_m)

  num_sms = get_num_sms()
  cluster_size = 1 + (config.cluster_dimension is not None)
  compiler_params = plgpu.CompilerParams(
      lowering_semantics=plgpu.LoweringSemantics.Warpgroup
  )
  f = plgpu.kernel(
      functools.partial(kernel, config=config),
      out_type=jax.ShapeDtypeStruct((m, n), out_dtype),
      grid=(num_sms // cluster_size,),
      grid_names=("cluster_grid",),
      cluster=(cluster_size,),
      cluster_names=("cluster",),
      num_threads=3,
      thread_name="wg",
      compiler_params=compiler_params,
  )
  return f(a, b, c)


def matmul(
    x: jax.Array,
    y: jax.Array,
    *,
    block_shape,
    block_k: int = 256,
    out_dtype: jnp.dtype | None = None,
    debug: bool = False,
) -> jax.Array:
  if out_dtype is None:
    if x.dtype != y.dtype:
      # TODO(tlongeri): Maybe we could use a deduction similar to jnp.dot
      raise TypeError(
          f"Cannot deduce output dtype for different input dtypes: {x.dtype},"
          f" {y.dtype}"
      )
    out_dtype = x.dtype
  acc_dtype = jnp.float32
  if x.dtype in [jnp.int8, jnp.int4, jnp.uint8, jnp.uint4]:
    acc_dtype = jnp.int32

  l, r = block_shape
  return pl.pallas_call(
      matmul_kernel,
      out_shape=jax.ShapeDtypeStruct((x.shape[0], y.shape[1]), out_dtype),
      grid_spec=pltpu.PrefetchScalarGridSpec(
          num_scalar_prefetch=0,
          in_specs=[
              pl.BlockSpec((l, block_k), lambda i, _, k: (i, k)),
              pl.BlockSpec((block_k, r), lambda _, j, k: (k, j)),
          ],
          out_specs=pl.BlockSpec((l, r), lambda i, j, k: (i, j)),
          grid=(x.shape[0] // l, y.shape[1] // r, x.shape[1] // block_k),
          scratch_shapes=[pltpu.VMEM((l, r), acc_dtype)],
      ),
      compiler_params=pltpu.CompilerParams(
          dimension_semantics=("parallel", "parallel", "arbitrary")),
      debug=debug,
  )(x, y)

