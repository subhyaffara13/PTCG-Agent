
def dropout(
    input: Tensor,
    p: float = 0.5,
    training: bool = True,
    inplace: bool = False,
) -> Tensor:
    r"""During training, randomly zeroes some elements of the input tensor with probability :attr:`p`.

    Uses samples from a Bernoulli distribution.

    See :class:`~torch.nn.Dropout` for details.

    Args:
        p: probability of an element to be zeroed. Default: 0.5
        training: apply dropout if is ``True``. Default: ``True``
        inplace: If set to ``True``, will do this operation in-place. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            dropout, (input,), input, p=p, training=training, inplace=inplace
        )
    if p < 0.0 or p > 1.0:
        raise ValueError(f"dropout probability has to be between 0 and 1, but got {p}")
    return (
        _VF.dropout_(input, p, training) if inplace else _VF.dropout(input, p, training)
    )


def dropout(input: Tensor, p: float, train: bool | None):
    if train and p != 0:
        return aten.native_dropout(input, p, train)[0]
    else:
        return input.clone()


def dropout(
    a: TensorLikeType, p: float = 0.5, training: bool = True, inplace: bool = False
) -> TensorLikeType:
    if inplace:
        raise NotImplementedError

    if not training:
        return a

    torch._check(
        p <= 1 and p >= 0,
        lambda: f"dropout probability has to be between 0 and 1, but got, {p}",
    )

    if p == 1:
        return torch.zeros_like(a)

    if p == 0:
        return a

    scale = 1 / (1 - p)
    dropout_mask = _dropout_helper(a, 1 - p)

    return a * dropout_mask * scale


def dropout(g: jit_utils.GraphContext, input, p, train):
    masked, _ = _dropout_returns_masked_input_and_mask(g, input, p, train)
    return masked


def dropout(g: jit_utils.GraphContext, input, p, train):
    symbolic_helper.check_training_mode(train, "dropout")
    # if train is False, dropout is no-op
    if not train:
        return input
    r, _ = g.op("Dropout", input, ratio_f=p, outputs=2)
    return r


def Dropout(rate, mode='train'):
  """Layer construction function for a dropout layer with given rate."""
  def init_fun(rng, input_shape):
    return input_shape, ()
  def apply_fun(params, inputs, **kwargs):
    rng = kwargs.get('rng', None)
    if rng is None:
      msg = ("Dropout layer requires apply_fun to be called with a PRNG key "
             "argument. That is, instead of `apply_fun(params, inputs)`, call "
             "it like `apply_fun(params, inputs, rng)` where `rng` is a "
             "PRNG key (e.g. from `jax.random.key`).")
      raise ValueError(msg)
    if mode == 'train':
      keep = random.bernoulli(rng, rate, inputs.shape)
      return jnp.where(keep, inputs / rate, 0)
    else:
      return inputs
  return init_fun, apply_fun


def dropout(scope, inputs, rate, deterministic=False, rng=None):
  """Applies a random dropout mask to the input.
  Args:
    inputs: the inputs that should be randomly masked.
    rate: the probablity of masking out a value.
    deterministic: if false the inputs are scaled by `1 / (1 - rate)` and
      masked, whereas if true, no mask is applied and the inputs are returned as
      is.
    rng: an optional `jax.random.PRNGKey`. By default `nn.make_rng()` will
      be used.
  Returns:
    The masked inputs.
  """
  if rate == 0.0:
    return inputs
  keep_prob = 1.0 - rate

  if deterministic:
    return inputs
  else:
    if rng is None:
      rng = scope.make_rng('dropout')
    mask = random.bernoulli(rng, p=keep_prob, shape=inputs.shape)
    return lax.select(mask, inputs / keep_prob, jnp.zeros_like(inputs))

