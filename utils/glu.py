
def glu(input: Tensor, dim: int = -1) -> Tensor:  # noqa: D400,D402
    r"""
    glu(input, dim=-1) -> Tensor

    The gated linear unit. Computes:

    .. math ::
        \text{GLU}(a, b) = a \otimes \sigma(b)

    where `input` is split in half along `dim` to form `a` and `b`, :math:`\sigma`
    is the sigmoid function and :math:`\otimes` is the element-wise product between matrices.

    See `Language Modeling with Gated Convolutional Networks <https://arxiv.org/abs/1612.08083>`_.

    Args:
        input (Tensor): input tensor
        dim (int): dimension on which to split the input. Default: -1
    """
    if has_torch_function_unary(input):
        return handle_torch_function(glu, (input,), input, dim=dim)
    if input.dim() == 0:
        raise RuntimeError(
            "glu does not support scalars because halving size must be even"
        )
    return torch._C._nn.glu(input, dim)


def glu(x, dim=-1):
    dim = _validate_dim(x, dim, 0)
    # TODO: don't guard on static shape here
    new_len = V.graph.sizevars.guard_int(x.get_size()[dim]) // 2
    # no need to clamp, index is int based on input size
    a = slice_(x, dim, 0, new_len, clamp=False)
    b = slice_(x, dim, new_len, new_len * 2, clamp=False)
    return mul(a, sigmoid(b))


def glu(a: TensorLikeType, dim: int = -1) -> TensorLikeType:
    dim = utils.canonicalize_dims(a.ndim, dim)
    torch._check(
        a.shape[dim] % 2 == 0,
        lambda: f"Halving dimension must be even, but dimension {dim} is size {a.shape[dim]}",
    )
    b, c = torch.tensor_split(a, 2, dim)

    return b * torch.sigmoid(c)


def glu(g: jit_utils.GraphContext, input, dim):
    dim_size = symbolic_helper._get_tensor_dim_size(input, dim)
    if dim_size is not None:
        if dim_size % 2 != 0:
            raise AssertionError(f"dim_size must be even, got {dim_size}")

    first, second = g.op("Split", input, axis_i=dim, outputs=2)
    return g.op("Mul", first, g.op("Sigmoid", second))


def glu(x: ArrayLike, axis: int = -1) -> Array:
  r"""Gated linear unit activation function.

  Computes the function:

  .. math::
    \mathrm{glu}(x) =  x\left[\ldots, 0:\frac{n}{2}, \ldots\right] \cdot
      \mathrm{sigmoid} \left( x\left[\ldots, \frac{n}{2}:n, \ldots\right]
        \right)

  where the array is split into two along ``axis``. The size of the ``axis``
  dimension must be divisible by two.

  Args:
    x : input array
    axis: the axis along which the split should be computed (default: -1)

  Returns:
    An array.

  See also:
    :func:`sigmoid`
  """
  x_arr = numpy_util.ensure_arraylike("glu", x)
  size = x_arr.shape[axis]
  assert size % 2 == 0, "axis size must be divisible by 2"
  x1, x2 = jnp.split(x_arr, 2, axis)
  return x1 * sigmoid(x2)

