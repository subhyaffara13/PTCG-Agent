
def micro_grad(
    fun: Function,
    has_aux: bool = False,
    argnums: int | Sequence[int] = 0,
    *,
    batch_argnums: int | Sequence[int] = 1,
    keep_batch_dim: bool = True,
    microbatch_size: int | None = None,
    accumulator: (
        Accumulator | AccumulationType | AccumulatorTree
    ) = AccumulationType.SUM,
    transform_fn: Callable[[base.ArrayTree], base.ArrayTree] = lambda x: x,
    metrics_fn: Callable[[base.ArrayTree], base.ArrayTree] = lambda x: None,
    num_real_microbatches: int | jax.Array | None = None,
) -> ValueAndGradFn:
  """Create a function to compute, transform, and sum per-example gradients.

  This function is similar to jax.value_and_grad, but works at the level of
  size-1 batches.  This function is defined in terms of general transformations
  transform_fn and metrics_fn which  can be useful to e.g.,
  * limit the effect of outlier batch elements by clipping per-example grads.
  * compute moments of the gradients on a per-example basis.
  * computing scalar or low-dimensional gradient metrics on a per-example basis.

  Other notable differences between this function and jax.value_and_grad:
  * at least one argument to `fun` must have a batch axis, and that argument
    should be passed to `batch_argnums`. The default value of `1` assumes that
    `fun` has the signature `fun(params, batch, ...)`.
  * The return signature is different. The gradient is always returned as the
    first output, while all auxiliary outputs are returned as a namedtuple in
    the second output (including values, function aux, and metrics).
  * This function may be able to work for far larger batch sizes than
    native jax.value_and_grad due to the built-in microbatching.

  Example Usage (see https://arxiv.org/abs/2510.00236):
    >>> import optax
    >>> def mean_squared_loss(params, features, targets):
    ...   preds = features @ params
    ...   diff = preds - targets
    ...   return 0.5 * jnp.mean(diff**2)
    >>> params = jnp.zeros(1)
    >>> features = jnp.ones((4, 1))
    >>> targets = jnp.array([0, 2, 4, 6])
    >>> (grads, squared_grads), aux = optax.microbatching.micro_grad(
    ...     mean_squared_loss,
    ...     argnums=0,
    ...     batch_argnums=(1,2),
    ...     accumulator=optax.microbatching.AccumulationType.MEAN,
    ...     transform_fn=lambda x: (x, x**2),
    ...     metrics_fn=jnp.linalg.norm
    ... )(params, features, targets)
    >>> grads, squared_grads  # per-example grads are [0, 2, 4, 6]
    (Array([-3.], dtype=float32), Array([14.], dtype=float32))
    >>> aux.values
    Array([ 0.,  2.,  8., 18.], dtype=float32)
    >>> aux.metrics
    Array([0., 2., 4., 6.], dtype=float32)


  Args:
    fun: The function to compute the gradient of.
    has_aux: Whether the function returns auxiliary output.
    argnums: The indices of argument(s) to differentiate with respect to.
    batch_argnums: The indices of argument(s) with a batch axis.
    keep_batch_dim: Whether `fun` expects inputs to have a batch dimension.
    microbatch_size: The size of the microbatches to use when computing the
      per-example gradients. See `microbatch` for more details.
    accumulator: Specifies how to combine or aggregate the transformed gradients
      across the batch axis.
    transform_fn: A function to apply to per-example gradients before averaging.
    metrics_fn: A function to apply to per-example gradients before
      transforming. Will be returned on a per-example basis as part of the
      auxiliary output, and therefore should be scalar or low-dimensional.
    num_real_microbatches: Optional number of microbatches that are actually
      executed. If specified, microbatching will terminate early after this
      many steps. Can be helpful to handle variable batch sizes without
      recompilation.

  Returns:
    A function that computes the value and gradient of `fun`, averaging the
    results over microbatches and applying the `transform_fn` and `metrics_fn`
    as described above. The auxiliary output (including values, metrics,
    function aux) will all be returned on a per-example-basis.
  """

  if isinstance(batch_argnums, int):
    batch_argnums = (batch_argnums,)

  fun = _normalize_fun_to_return_aux(fun, has_aux)
  value_and_grad_fn = jax.value_and_grad(fun, argnums, has_aux=True)

  def grad_fn(*args, **kwargs):
    value_and_aux, grad = value_and_grad_fn(*args, **kwargs)
    result = transform_fn(grad)
    aux = IndividualOutputs(
        values=value_and_aux[0],
        metrics=metrics_fn(grad),
        aux=value_and_aux[1],
    )
    return result, aux

  in_axes = [None] * (max(batch_argnums) + 1)
  for i in batch_argnums:
    in_axes[i] = 0
  micro_fun = micro_vmap(
      grad_fn,
      in_axes=in_axes,
      accumulator=(accumulator, AccumulationType.CONCAT),
      microbatch_size=microbatch_size,
      num_real_microbatches=num_real_microbatches,
  )
  if keep_batch_dim:
    micro_fun = _with_extra_batch_axis(micro_fun, batch_argnums)
  return micro_fun

