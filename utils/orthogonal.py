
def orthogonal(
    module: Module,
    name: str = "weight",
    orthogonal_map: str | None = None,
    *,
    use_trivialization: bool = True,
) -> Module:
    r"""Apply an orthogonal or unitary parametrization to a matrix or a batch of matrices.

    Letting :math:`\mathbb{K}` be :math:`\mathbb{R}` or :math:`\mathbb{C}`, the parametrized
    matrix :math:`Q \in \mathbb{K}^{m \times n}` is **orthogonal** as

    .. math::

        \begin{align*}
            Q^{\text{H}}Q &= \mathrm{I}_n \mathrlap{\qquad \text{if }m \geq n}\\
            QQ^{\text{H}} &= \mathrm{I}_m \mathrlap{\qquad \text{if }m < n}
        \end{align*}

    where :math:`Q^{\text{H}}` is the conjugate transpose when :math:`Q` is complex
    and the transpose when :math:`Q` is real-valued, and
    :math:`\mathrm{I}_n` is the `n`-dimensional identity matrix.
    In plain words, :math:`Q` will have orthonormal columns whenever :math:`m \geq n`
    and orthonormal rows otherwise.

    If the tensor has more than two dimensions, we consider it as a batch of matrices of shape `(..., m, n)`.

    The matrix :math:`Q` may be parametrized via three different ``orthogonal_map`` in terms of the original tensor:

    - ``"matrix_exp"``/``"cayley"``:
      the :func:`~torch.matrix_exp` :math:`Q = \exp(A)` and the `Cayley map`_
      :math:`Q = (\mathrm{I}_n + A/2)(\mathrm{I}_n - A/2)^{-1}` are applied to a skew-symmetric
      :math:`A` to give an orthogonal matrix.
    - ``"householder"``: computes a product of Householder reflectors
      (:func:`~torch.linalg.householder_product`).

    ``"matrix_exp"``/``"cayley"`` often make the parametrized weight converge faster than
    ``"householder"``, but they are slower to compute for very thin or very wide matrices.

    If ``use_trivialization=True`` (default), the parametrization implements the "Dynamic Trivialization Framework",
    where an extra matrix :math:`B \in \mathbb{K}^{n \times n}` is stored under
    ``module.parametrizations.weight[0].base``. This helps the
    convergence of the parametrized layer at the expense of some extra memory use.
    See `Trivializations for Gradient-Based Optimization on Manifolds`_ .

    Initial value of :math:`Q`:
    If the original tensor is not parametrized and ``use_trivialization=True`` (default), the initial value
    of :math:`Q` is that of the original tensor if it is orthogonal (or unitary in the complex case)
    and it is orthogonalized via the QR decomposition otherwise (see :func:`torch.linalg.qr`).
    Same happens when it is not parametrized and ``orthogonal_map="householder"`` even when ``use_trivialization=False``.
    Otherwise, the initial value is the result of the composition of all the registered
    parametrizations applied to the original tensor.

    .. note::
        This function is implemented using the parametrization functionality
        in :func:`~torch.nn.utils.parametrize.register_parametrization`.


    .. _`Cayley map`: https://en.wikipedia.org/wiki/Cayley_transform#Matrix_map
    .. _`Trivializations for Gradient-Based Optimization on Manifolds`: https://arxiv.org/abs/1909.09501

    Args:
        module (nn.Module): module on which to register the parametrization.
        name (str, optional): name of the tensor to make orthogonal. Default: ``"weight"``.
        orthogonal_map (str, optional): One of the following: ``"matrix_exp"``, ``"cayley"``, ``"householder"``.
            Default: ``"matrix_exp"`` if the matrix is square or complex, ``"householder"`` otherwise.
        use_trivialization (bool, optional): whether to use the dynamic trivialization framework.
            Default: ``True``.

    Returns:
        The original module with an orthogonal parametrization registered to the specified
        weight

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_LAPACK)
        >>> orth_linear = orthogonal(nn.Linear(20, 40))
        >>> orth_linear
        ParametrizedLinear(
        in_features=20, out_features=40, bias=True
        (parametrizations): ModuleDict(
            (weight): ParametrizationList(
            (0): _Orthogonal()
            )
        )
        )
        >>> # xdoctest: +IGNORE_WANT
        >>> Q = orth_linear.weight
        >>> torch.dist(Q.T @ Q, torch.eye(20))
        tensor(4.9332e-07)
    """
    weight = getattr(module, name, None)
    if not isinstance(weight, Tensor):
        raise ValueError(
            f"Module '{module}' has no parameter or buffer with name '{name}'"
        )

    # We could implement this for 1-dim tensors as the maps on the sphere
    # but I believe it'd bite more people than it'd help
    if weight.ndim < 2:
        raise ValueError(
            "Expected a matrix or batch of matrices. "
            f"Got a tensor of {weight.ndim} dimensions."
        )

    if orthogonal_map is None:
        orthogonal_map = (
            "matrix_exp"
            if weight.size(-2) == weight.size(-1) or weight.is_complex()
            else "householder"
        )

    orth_enum = getattr(_OrthMaps, orthogonal_map, None)
    if orth_enum is None:
        raise ValueError(
            'orthogonal_map has to be one of "matrix_exp", "cayley", "householder". '
            f"Got: {orthogonal_map}"
        )
    orth = _Orthogonal(weight, orth_enum, use_trivialization=use_trivialization)
    parametrize.register_parametrization(module, name, orth, unsafe=True)
    return module


def orthogonal(scale: RealNumeric = 1.0,
               column_axis: int = -1,
               dtype: DTypeLikeInexact | None = None) -> Initializer:
  """
  Builds an initializer that returns uniformly distributed orthogonal matrices.

  If the shape is not square, the matrices will have orthonormal rows or columns
  depending on which side is smaller.

  Args:
    scale: the upper bound of the uniform distribution.
    column_axis: the axis that contains the columns that should be orthogonal.
    dtype: the default dtype of the weights.

  Returns:
    An orthogonal initializer.

  Examples:

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.orthogonal()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 3.9026976e-01,  7.2495741e-01, -5.6756169e-01],
         [ 8.8047469e-01, -4.7409311e-01, -1.3157725e-04]],            dtype=float32)
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    if out_sharding is not None:
      raise NotImplementedError
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    if len(shape) < 2:
      raise ValueError("orthogonal initializer requires at least a 2D shape")

    if any(dim == 0 for dim in shape):
      # empty shape
      return jnp.zeros(shape, dtype=dtype, out_sharding=out_sharding)

    n_rows, n_cols = math.prod(shape) // shape[column_axis], shape[column_axis]
    Q = random.orthogonal(key, n_rows, (), dtype, n_cols)
    Q = jnp.reshape(Q, tuple(np.delete(shape, column_axis)) + (shape[column_axis],))
    Q = jnp.moveaxis(Q, -1, column_axis)
    return jnp.array(scale, dtype) * Q
  return init


def orthogonal(
  key: ArrayLike,
  n: int,
  shape: Shape = (),
  dtype: DTypeLikeFloat | None = None,
  m: int | None = None,
  *,
  out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample uniformly from the orthogonal group O(n).

  If the dtype is complex, sample uniformly from the unitary group U(n).

  For unequal rows and columns, this samples a semi-orthogonal matrix instead.
  That is, if :math:`A` is the resulting matrix and :math:`A^*` is its conjugate
  transpose, then:

  - If :math:`n \leq m`, the rows are mutually orthonormal: :math:`A A^* = I_n`.
  - If :math:`m \leq n`, the columns are mutually orthonormal: :math:`A^* A = I_m`.

  Args:
    key: a PRNG key used as the random key.
    n: an integer indicating the number of rows.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    m: an integer indicating the number of columns. Defaults to `n`.
    out_sharding: optional, specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array of shape `(*shape, n, m)` and specified dtype.

  References:
    .. [1] Mezzadri, Francesco. (2007). "How to generate random matrices from
           the classical compact groups". Notices of the American Mathematical
           Society, 54(5), 592-604. https://arxiv.org/abs/math-ph/0609050.
  """
  if m is None:
    _m = n
  else:
    _m = m
  shape = core.canonicalize_shape(shape)
  key, _ = _check_prng_key("orthogonal", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  _check_shape("orthogonal", shape)
  n = core.concrete_or_error(index, n, "The error occurred in jax.random.orthogonal()")
  _m = core.concrete_or_error(index, _m, "The error occurred in jax.random.orthogonal()")
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "orthogonal", shape)
  return maybe_auto_axes(_orthogonal, out_sharding, n=n, _m=_m, shape=shape, dtype=dtype)(key)

