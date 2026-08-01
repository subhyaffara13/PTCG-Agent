
def scatter_add(x, dim: int, index, src):
    return scatter_add_(clone(x), dim, index, src)


def scatter_add(g: jit_utils.GraphContext, self, dim, index, src):
    src_type = _type_utils.JitScalarType.from_value(
        src, _type_utils.JitScalarType.UNDEFINED
    )
    src_sizes = symbolic_helper._get_tensor_sizes(src)
    index_sizes = symbolic_helper._get_tensor_sizes(index)

    if len(src_sizes) != len(index_sizes):
        return symbolic_helper._unimplemented(
            "scatter_add",
            f"`index` ({index_sizes}) should have the same dimensionality as `src` ({src_sizes})",
        )

    # PyTorch only allows index shape <= src shape, so we can only consider
    # taking index as subset size to src, like PyTorch does. When sizes for src
    # and index are not matched or there are dynamic axes, we take index shape to
    # slice src to accommodate.
    if src_sizes != index_sizes or None in index_sizes:
        adjusted_shape = g.op("Shape", index)
        starts = g.op("Constant", value_t=torch.tensor([0] * len(index_sizes)))
        src = g.op("Slice", src, starts, adjusted_shape)

    src = symbolic_helper._maybe_get_scalar(src)
    if symbolic_helper._is_value(src):
        return g.op("ScatterElements", self, index, src, axis_i=dim, reduction_s="add")
    else:
        # Check if scalar "src" has same type as self (PyTorch allows different
        # type for scalar src (but not when src is tensor)). If not, insert Cast node.
        if _type_utils.JitScalarType.from_value(self) != src_type:
            src = g.op(
                "Cast",
                src,
                to_i=_type_utils.JitScalarType.from_value(self).onnx_type(),
            )

        return g.op(
            "ScatterElements",
            self,
            index,
            src,
            axis_i=dim,
            reduction_s="add",
        )


def scatter_add(g: jit_utils.GraphContext, self, dim, index, src):
    scalar_type = symbolic_helper._try_get_scalar_type(self)
    if scalar_type is None:
        return symbolic_helper._unimplemented(
            "scatter_add", "input dtype not accessible", self
        )
    sizes = symbolic_helper._get_tensor_sizes(self, allow_nonstatic=False)
    if sizes:
        to_add = g.op("Constant", value_t=torch.zeros(sizes, dtype=scalar_type.dtype()))
    else:
        to_add = zeros_like(g, self, scalar_type)
    to_add = symbolic_helper._scatter_helper(g, to_add, dim, index, src)
    return add(g, self, to_add)


def scatter_add(
  operand: ArrayLike, scatter_indices: ArrayLike, updates: ArrayLike,
  dimension_numbers: ScatterDimensionNumbers, *,
  indices_are_sorted: bool = False, unique_indices: bool = False,
  mode: str | GatherScatterMode | None = None) -> Array:
  """Scatter-add operator.

  Wraps `XLA's Scatter operator
  <https://www.openxla.org/xla/operation_semantics#scatter>`_, where
  addition is used to combine updates and values from `operand`.

  The semantics of scatter are complicated, and its API might change in the
  future. For most use cases, you should prefer the
  :attr:`jax.numpy.ndarray.at` property on JAX arrays which uses
  the familiar NumPy indexing syntax.

  Args:
    operand: an array to which the scatter should be applied
    scatter_indices: an array that gives the indices in `operand` to which each
      update in `updates` should be applied.
    updates: the updates that should be scattered onto `operand`.
    dimension_numbers: a `lax.ScatterDimensionNumbers` object that describes how
      dimensions of `operand`, `scatter_indices`, `updates` and the output
      relate.
    indices_are_sorted: whether `scatter_indices` is known to be sorted. If
      true, may improve performance on some backends.
    unique_indices: whether the elements to be updated in ``operand`` are
      guaranteed to not overlap with each other. If true, may improve
      performance on some backends. JAX does not check this promise: if the
      updated elements overlap when ``unique_indices`` is ``True`` the behavior
      is undefined.
    mode: how to handle indices that are out of bounds: when set to 'clip',
      indices are clamped so that the slice is within bounds, and when set to
      'fill' or 'drop' out-of-bounds updates are dropped. The behavior for
      out-of-bounds indices when set to 'promise_in_bounds' is
      implementation-defined.

  Returns:
    An array containing the sum of `operand` and the scattered updates.

  Examples:
    As mentioned above, you should basically never use :func:`scatter_add`
    directly, and instead perform scatter-style operations using NumPy-style
    indexing expressions via :attr:`jax.numpy.ndarray.at`.

    Here is and example of updating entries in an array using
    :attr:`jax.numpy.ndarray.at`, which lowers to an XLA Scatter operation:

    >>> x = jnp.ones(5)
    >>> indices = jnp.array([1, 2, 4])
    >>> values = jnp.array([2.0, 3.0, 4.0])

    >>> x.at[indices].add(values)
    Array([1., 3., 4., 1., 5.], dtype=float32)

    This syntax also supports several of the optional arguments to
    :func:`scatter_add`, for example:

    >>> x.at[indices].add(values, indices_are_sorted=True,
    ...                   mode='promise_in_bounds')
    Array([1., 3., 4., 1., 5.], dtype=float32)

    By comparison, here is the equivalent function call using
    :func:`scatter_add` directly, which is not something typical users should
    ever need to do:

    >>> lax.scatter_add(x, indices[:, None], values,
    ...                 dimension_numbers=lax.ScatterDimensionNumbers(
    ...                     update_window_dims=(),
    ...                     inserted_window_dims=(0,),
    ...                     scatter_dims_to_operand_dims=(0,)),
    ...                 indices_are_sorted=True,
    ...                 mode=lax.GatherScatterMode.PROMISE_IN_BOUNDS)
    Array([1., 3., 4., 1., 5.], dtype=float32)
  """
  jaxpr, consts = lax._reduction_jaxpr(lax.add, typeof(lax._const(operand, 0)))
  operand, scatter_indices, updates = core.auto_insert_reshard(
      operand, scatter_indices, updates)
  return scatter_add_p.bind(
      operand, scatter_indices, updates, update_jaxpr=jaxpr,
      update_consts=consts, dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=GatherScatterMode.from_any(mode))

