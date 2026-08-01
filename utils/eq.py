
def eq(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.eq(a, b)


def eq(left, right):
    return V.graph.sizevars.guard_or_false(sympy.Eq(left, right))


def eq(g: jit_utils.GraphContext, self, other):
    if isinstance(self.type(), _C.DeviceObjType) and isinstance(
        other.type(), _C.DeviceObjType
    ):
        # ONNX doesn't have devices, so consider them all to be equal.
        # The no-op check for equality will get constant-folded.
        return g.op("Constant", value_t=torch.tensor(True, dtype=torch.bool))
    self_node = self.node()
    other_node = other.node()
    if self_node.kind() == other_node.kind() == "onnx::Constant":
        if self_node.kindOf("value") == other_node.kindOf("value") == "s":
            # Exporting strings to ONNX is not supported.
            # If both strings are constant, we can compare them directly.
            # The no-op check for equality will get constant-folded.
            return g.op(
                "Constant",
                value_t=torch.tensor(
                    self_node.s("value") == other_node.s("value"),
                    dtype=torch.bool,
                ),
            )

    return g.op("Equal", self, other)


def eq(a, b, tol=1e-6):
    for u, v in zip(a, b):
        if not (abs(u - v) < tol):
            return False
    return True


def eq(a, b, tol=1e-6):
    for x, y in zip(a, b):
        if not (abs(x - y) < tol):
            return False
    return True


def eq(v, w, msg=''):
    result = allclose(v, w)
    if not result:
        print(f'Not eq:{msg}\n{v}\n----{w}')
    return result


def eq(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise equals: :math:`x = y`.

  This function lowers directly to the `stablehlo.compare`_ operation
  with ``comparison_direction=EQ`` and ``compare_type`` set according
  to the input dtype.

  Args:
    x, y: Input arrays. Must have matching dtypes. If neither is a
      scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    A boolean array of shape ``lax.broadcast_shapes(x.shape, y.shape)``
    containing the elementwise equal comparison.

  See also:
    - :func:`jax.numpy.equal`: NumPy wrapper for this API, also accessible
      via the ``x == y`` operator on JAX arrays.
    - :func:`jax.lax.ne`: elementwise not-equal
    - :func:`jax.lax.ge`: elementwise greater-than-or-equal
    - :func:`jax.lax.gt`: elementwise greater-than
    - :func:`jax.lax.le`: elementwise less-than-or-equal
    - :func:`jax.lax.lt`: elementwise less-than

  .. _stablehlo.compare: https://openxla.org/stablehlo/spec#compare
  """
  x, y = core.auto_insert_reshard(x, y)
  return eq_p.bind(x, y)

