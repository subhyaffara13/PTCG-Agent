
def meshgrid(*tensors: torch.Tensor | list[torch.Tensor], indexing: str | None = None) -> tuple[torch.Tensor, ...]:
    """
    Wrapper around torch.meshgrid to avoid warning messages about the introduced `indexing` argument.

    Reference: https://pytorch.org/docs/1.13/generated/torch.meshgrid.html
    """
    return torch.meshgrid(*tensors, indexing=indexing)


def meshgrid(*xi: ArrayLike, copy=True, sparse=False, indexing="xy"):
    ndim = len(xi)

    if indexing not in ["xy", "ij"]:
        raise ValueError("Valid values for `indexing` are 'xy' and 'ij'.")

    s0 = (1,) * ndim
    output = [x.reshape(s0[:i] + (-1,) + s0[i + 1 :]) for i, x in enumerate(xi)]

    if indexing == "xy" and ndim > 1:
        # switch first and second axis
        output[0] = output[0].reshape((1, -1) + s0[2:])
        output[1] = output[1].reshape((-1, 1) + s0[2:])

    if not sparse:
        # Return the full N-D matrix (not only the 1-D vector)
        output = torch.broadcast_tensors(*output)

    if copy:
        output = [x.clone() for x in output]

    return list(output)  # match numpy, return a list


def meshgrid(tensors: Sequence[TensorLikeType], indexing: str):
    pass


def meshgrid(*tensors: TensorLikeType, indexing: str):
    pass


def meshgrid(
    *tensors: TensorLikeType | list[TensorLikeType] | tuple[TensorLikeType],
    indexing: str,
) -> list[TensorLikeType]:
    # This ref simultaneously handles two overloads (see stubs above)
    # The `indexing` argument is currently optional for torch.meshgrid, but we
    # plan to make the argument required: https://github.com/pytorch/pytorch/issues/50276
    if isinstance(tensors[0], (list, tuple)):
        if len(tensors) != 1:
            raise AssertionError(
                f"Expected exactly 1 tensor list/tuple, got {len(tensors)}"
            )
        tensors = tuple(tensors[0])

    torch._check(
        builtins.all(isinstance(a, TensorLike) for a in tensors),
        lambda: "meshgrid expects its inputs to be tensors",
    )

    torch._check(len(tensors) > 0, lambda: "meshgrid expects a non-empty TensorList")

    for i in range(len(tensors) - 1):
        torch._check(
            tensors[i].dtype == tensors[i + 1].dtype,  # type: ignore[union-attr]
            lambda: "meshgrid expects all tensors to have the same dtype",
        )
        torch._check(
            tensors[i].device == tensors[i + 1].device,  # type: ignore[union-attr]
            lambda: "meshgrid expects all tensors to have the same device",
        )

    swap_first_and_second_tensors = False
    if indexing == "xy":
        swap_first_and_second_tensors = len(tensors) >= 2
        if swap_first_and_second_tensors:
            tensors = (tensors[1], tensors[0], *tensors[2:])
    else:
        torch._check(
            indexing == "ij",
            lambda: (
                'torch.meshgrid: indexing must be one of "xy" or "ij", '
                f"but received: {indexing}"
            ),
        )

    result_shape: list[int] = []
    for t in tensors:
        if not isinstance(t, TensorLike):
            raise AssertionError(f"expected TensorLike, got {type(t)}")  # mypy
        torch._check(
            t.ndim == 0 or t.ndim == 1,
            lambda: f"torch.meshgrid: Expected 0D or 1D tensor in the tensor list but got: {t}",
        )
        result_shape.append(t.numel())

    grids: list[TensorLikeType] = []
    for i, t in enumerate(tensors):
        if not isinstance(t, TensorLike):
            raise AssertionError(f"expected TensorLike, got {type(t)}")  # mypy
        if t.ndim == 0:
            t = t.view((1,))
        grids.append(prims.broadcast_in_dim(t, result_shape, (i,)))

    if swap_first_and_second_tensors:
        # Swap outputs if we originally swapped at the beginning
        grids[0], grids[1] = grids[1], grids[0]

    return grids


def meshgrid(g: jit_utils.GraphContext, tensor_list, indexing: str | None = None):
    if indexing is None:
        indexing = "ij"
    elif indexing not in {"ij", "xy"}:
        raise errors.SymbolicValueError(
            f"Unsupported indexing: {indexing}", tensor_list
        )
    unpacked_tensor_list = symbolic_helper._unpack_list(tensor_list)
    if indexing == "xy":
        unpacked_tensor_list[:2] = unpacked_tensor_list[1::-1]
    tensors = [
        symbolic_helper._reshape_helper(
            g, t, g.op("Constant", value_t=torch.LongTensor([-1]))
        )
        for t in unpacked_tensor_list
    ]
    tensors_shape = [g.op("Shape", t) for t in tensors]
    out_shape = g.op("Concat", *tensors_shape, axis_i=0)
    out = []
    for i, t in enumerate(tensors):
        shape_i = [g.op("Constant", value_t=torch.ones(1, dtype=torch.int64))] * len(
            tensors
        )
        shape_i[i] = tensors_shape[i]
        t_reshaped = _reshape_from_tensor(g, t, g.op("Concat", *shape_i, axis_i=0))
        out.append(g.op("Expand", t_reshaped, out_shape))
    if indexing == "xy":
        out[0], out[1] = out[1], out[0]
    return g.op("prim::ListConstruct", *out)


def meshgrid(*arrays: Array, indexing: Literal['xy', 'ij'] = 'xy') -> tuple[Array, ...]:
    return tuple(cp.meshgrid(*arrays, indexing=indexing))


def meshgrid(*arrays: Array, indexing: Literal['xy', 'ij'] = 'xy') -> tuple[Array, ...]:
    # torch <= 2.9 emits a UserWarning: "torch.meshgrid: in an upcoming release, it
    # will be required to pass the indexing argument."
    # Thus always pass it explicitly.
    return torch.meshgrid(*arrays, indexing=indexing)


def meshgrid(*xi, copy=True, sparse=False, indexing='xy'):
    """
    Return a tuple of coordinate matrices from coordinate vectors.

    Make N-D coordinate arrays for vectorized evaluations of
    N-D scalar/vector fields over N-D grids, given
    one-dimensional coordinate arrays x1, x2,..., xn.

    Parameters
    ----------
    x1, x2,..., xn : array_like
        1-D arrays representing the coordinates of a grid.
    indexing : {'xy', 'ij'}, optional
        Cartesian ('xy', default) or matrix ('ij') indexing of output.
        See Notes for more details.
    sparse : bool, optional
        If True the shape of the returned coordinate array for dimension *i*
        is reduced from ``(N1, ..., Ni, ... Nn)`` to
        ``(1, ..., 1, Ni, 1, ..., 1)``.  These sparse coordinate grids are
        intended to be used with :ref:`basics.broadcasting`.  When all
        coordinates are used in an expression, broadcasting still leads to a
        fully-dimensional result array.

        Default is False.

    copy : bool, optional
        If False, a view into the original arrays are returned in order to
        conserve memory.  Default is True.  Please note that
        ``sparse=False, copy=False`` will likely return non-contiguous
        arrays.  Furthermore, more than one element of a broadcast array
        may refer to a single memory location.  If you need to write to the
        arrays, make copies first.

    Returns
    -------
    X1, X2,..., XN : tuple of ndarrays
        For vectors `x1`, `x2`,..., `xn` with lengths ``Ni=len(xi)``,
        returns ``(N1, N2, N3,..., Nn)`` shaped arrays if indexing='ij'
        or ``(N2, N1, N3,..., Nn)`` shaped arrays if indexing='xy'
        with the elements of `xi` repeated to fill the matrix along
        the first dimension for `x1`, the second for `x2` and so on.

    Notes
    -----
    This function supports both indexing conventions through the indexing
    keyword argument.  Giving the string 'ij' returns a meshgrid with
    matrix indexing, while 'xy' returns a meshgrid with Cartesian indexing.
    In the 2-D case with inputs of length M and N, the outputs are of shape
    (N, M) for 'xy' indexing and (M, N) for 'ij' indexing.  In the 3-D case
    with inputs of length M, N and P, outputs are of shape (N, M, P) for
    'xy' indexing and (M, N, P) for 'ij' indexing.  The difference is
    illustrated by the following code snippet::

        xv, yv = np.meshgrid(x, y, indexing='ij')
        for i in range(nx):
            for j in range(ny):
                # treat xv[i,j], yv[i,j]

        xv, yv = np.meshgrid(x, y, indexing='xy')
        for i in range(nx):
            for j in range(ny):
                # treat xv[j,i], yv[j,i]

    In the 1-D and 0-D case, the indexing and sparse keywords have no effect.

    See Also
    --------
    mgrid : Construct a multi-dimensional "meshgrid" using indexing notation.
    ogrid : Construct an open multi-dimensional "meshgrid" using indexing
            notation.
    :ref:`how-to-index`

    Examples
    --------
    >>> import numpy as np
    >>> nx, ny = (3, 2)
    >>> x = np.linspace(0, 1, nx)
    >>> y = np.linspace(0, 1, ny)
    >>> xv, yv = np.meshgrid(x, y)
    >>> xv
    array([[0. , 0.5, 1. ],
           [0. , 0.5, 1. ]])
    >>> yv
    array([[0.,  0.,  0.],
           [1.,  1.,  1.]])

    The result of `meshgrid` is a coordinate grid:

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(xv, yv, marker='o', color='k', linestyle='none')
    >>> plt.show()

    You can create sparse output arrays to save memory and computation time.

    >>> xv, yv = np.meshgrid(x, y, sparse=True)
    >>> xv
    array([[0. ,  0.5,  1. ]])
    >>> yv
    array([[0.],
           [1.]])

    `meshgrid` is very useful to evaluate functions on a grid. If the
    function depends on all coordinates, both dense and sparse outputs can be
    used.

    >>> x = np.linspace(-5, 5, 101)
    >>> y = np.linspace(-5, 5, 101)
    >>> # full coordinate arrays
    >>> xx, yy = np.meshgrid(x, y)
    >>> zz = np.sqrt(xx**2 + yy**2)
    >>> xx.shape, yy.shape, zz.shape
    ((101, 101), (101, 101), (101, 101))
    >>> # sparse coordinate arrays
    >>> xs, ys = np.meshgrid(x, y, sparse=True)
    >>> zs = np.sqrt(xs**2 + ys**2)
    >>> xs.shape, ys.shape, zs.shape
    ((1, 101), (101, 1), (101, 101))
    >>> np.array_equal(zz, zs)
    True

    >>> h = plt.contourf(x, y, zs)
    >>> plt.axis('scaled')
    >>> plt.colorbar()
    >>> plt.show()
    """
    ndim = len(xi)

    if indexing not in ['xy', 'ij']:
        raise ValueError(
            "Valid values for `indexing` are 'xy' and 'ij'.")

    s0 = (1,) * ndim
    output = [np.asanyarray(x).reshape(s0[:i] + (-1,) + s0[i + 1:])
              for i, x in enumerate(xi)]

    if indexing == 'xy' and ndim > 1:
        # switch first and second axis
        output[0] = output[0].reshape((1, -1) + s0[2:])
        output[1] = output[1].reshape((-1, 1) + s0[2:])

    if not sparse:
        # Return the full N-D matrix (not only the 1-D vector)
        output = np.broadcast_arrays(*output, subok=True)

    if copy:
        output = tuple(x.copy() for x in output)

    if sparse and not copy:
        return tuple(output)

    return output


def meshgrid(*xi: ArrayLike, copy: bool = True, sparse: bool = False,
             indexing: str = 'xy') -> list[Array]:
  """Construct N-dimensional grid arrays from N 1-dimensional vectors.

  JAX implementation of :func:`numpy.meshgrid`.

  Args:
    xi: N arrays to convert to a grid.
    copy: whether to copy the input arrays. JAX supports only ``copy=True``,
      though under JIT compilation the compiler may opt to avoid copies.
    sparse: if False (default), then each returned arrays will be of shape
      ``[len(x1), len(x2), ..., len(xN)]``. If False, then returned arrays
      will be of shape ``[1, 1, ..., len(xi), ..., 1, 1]``.
    indexing: options are ``'xy'`` for cartesian indexing (default) or ``'ij'``
      for matrix indexing.

  Returns:
    A length-N list of grid arrays.

  See also:
    - :func:`jax.numpy.indices`: generate a grid of indices.
    - :obj:`jax.numpy.mgrid`: create a meshgrid using indexing syntax.
    - :obj:`jax.numpy.ogrid`: create an open meshgrid using indexing syntax.

  Examples:
    For the following examples, we'll use these 1D arrays as inputs:

    >>> x = jnp.array([1, 2])
    >>> y = jnp.array([10, 20, 30])

    2D cartesian mesh grid:

    >>> x_grid, y_grid = jnp.meshgrid(x, y)
    >>> print(x_grid)
    [[1 2]
     [1 2]
     [1 2]]
    >>> print(y_grid)
    [[10 10]
     [20 20]
     [30 30]]

    2D sparse cartesian mesh grid:

    >>> x_grid, y_grid = jnp.meshgrid(x, y, sparse=True)
    >>> print(x_grid)
    [[1 2]]
    >>> print(y_grid)
    [[10]
     [20]
     [30]]

    2D matrix-index mesh grid:

    >>> x_grid, y_grid = jnp.meshgrid(x, y, indexing='ij')
    >>> print(x_grid)
    [[1 1 1]
     [2 2 2]]
    >>> print(y_grid)
    [[10 20 30]
     [10 20 30]]
  """
  args = list(util.ensure_arraylike_tuple("meshgrid", tuple(xi)))
  if not copy:
    raise ValueError("jax.numpy.meshgrid only supports copy=True")
  if indexing not in ["xy", "ij"]:
    raise ValueError(f"Valid values for indexing are 'xy' and 'ij', got {indexing}")
  if any(a.ndim != 1 for a in args):
    raise ValueError("Arguments to jax.numpy.meshgrid must be 1D, got shapes "
                     f"{[a.shape for a in args]}")
  if indexing == "xy" and len(args) >= 2:
    args[0], args[1] = args[1], args[0]
  shape = [1 if sparse else a.shape[0] for a in args]
  _a_shape = lambda i, a: [*shape[:i], a.shape[0], *shape[i + 1:]] if sparse else shape
  output = [lax.broadcast_in_dim(a, _a_shape(i, a), (i,)) for i, a, in enumerate(args)]
  if indexing == "xy" and len(args) >= 2:
    output[0], output[1] = output[1], output[0]
  return output

