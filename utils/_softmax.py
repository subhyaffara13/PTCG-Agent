
def _softmax(x: Tensor, dim: int, half_to_float: bool):
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    # eager softmax returns a contiguous tensor. Ensure that decomp also returns
    # a contiguous tensor.
    x = x.contiguous()
    if half_to_float:
        if x.dtype != torch.half:
            raise AssertionError(
                f"half_to_float is True but x.dtype is {x.dtype}, expected torch.half"
            )
    computation_dtype, result_dtype = utils.elementwise_dtypes(
        x, type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
    x = x.to(computation_dtype)
    if guard_or_false(x.numel() == 0):
        unnormalized = torch.exp(x)
    else:
        x_max = torch.amax(x, dim, keepdim=True)
        unnormalized = torch.exp(x - x_max)
    result = unnormalized / torch.sum(unnormalized, dim, keepdim=True)
    if not half_to_float:
        result = result.to(result_dtype)
    return result


def _softmax(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=3, len_kwargs=0
    )
    data = _get_data(args[0])
    mask = _maybe_get_mask(args[0])
    result_data = torch.ops.aten._masked_softmax(data, ~mask, args[1], 2)
    return MaskedTensor(result_data, mask)


def _softmax(
    x: ArrayLike,
    axis: Axis = -1,
    where: ArrayLike | None = None,
    initial: ArrayLike = -np.inf) -> Array:
  x_max = jnp.max(x, axis, where=where, initial=initial, keepdims=True)
  x_safe = x if where is None else jnp.where(where, x, initial)
  unnormalized = jnp.exp(x_safe - x_max)
  result = unnormalized / jnp.sum(unnormalized, axis, where=where, keepdims=True)
  if where is not None:
    result = jnp.where(where, result, 0)
  return result

