
def microbatch(
    fun: Function,
    argnums: int | Sequence[int],
    microbatch_size: int | None,
    accumulator: (
        Accumulator | AccumulationType | AccumulatorTree
    ) = AccumulationType.SUM,
    *,
    argnames: str | Sequence[str] = (),
    in_axes: int | Sequence[int] = 0,
    num_real_microbatches: int | jax.Array | None = None,
) -> Function:
  """A general microbatching transformation.

  Conceptually, given ``fun``, this function returns a new function that does
  something like the following (for the case of SUM accumulator):

  .. code-block:: python

    def microbatched_fun(full_batch):
      accumulator = 0
      for microbatch in full_batch:
        accumulator += fun(microbatch)
      return accumulator

  where under the hood the ``for`` is implemented via a ``lax.fori_loop`` and
  hence forced to be sequential.

  This function is useful when evaluating ``fun`` on the full input batch
  exceeds available device memory. By splitting the batch into smaller
  microbatches and processing them sequentially, peak memory usage can be
  significantly reduced. Because the function is evaluated on smaller batches,
  this transformation requires knowledge of how the individual microbatch
  results should be combined back together (SUM, MEAN, or CONCAT). See the
  accumulator argument for more details.

  Example Usage:
    >>> import jax.numpy as jnp
    >>> fun = lambda x: (x+1, jnp.sum(3*x))
    >>> data = jnp.array([1, 2, 3, 4])
    >>> fun(data)
    (Array([2, 3, 4, 5], dtype=int32), Array(30, dtype=int32))
    >>> strategy = (
    ...    optax.microbatching.AccumulationType.CONCAT,
    ...    optax.microbatching.AccumulationType.SUM
    ... )
    >>> microbatched_fun = optax.microbatch(
    ...    fun, argnums=0, microbatch_size=2, accumulator=strategy
    ... )
    >>> microbatched_fun(data)
    (Array([2, 3, 4, 5], dtype=int32), Array(30, dtype=int32))

  Args:
      fun: An arbitrary function.
      argnums: A sequence of argument indices that have a batch axis.
      microbatch_size: The number of rows in the overall batch used in each
        microbatch. Smaller values reduce memory overhead, but require more
        sequential computation. This must evenly divide the batch axis size of
        the batch arguments.
      accumulator: Specifies how to combine results from each microbatch; can be
        a single `Accumulator`, a pytree matching the structure of `fun`'s
        output, with `Accumulator` values at the leaves, or anything in between
        (i.e., a PyTree prefix of `fun`'s output`).
      argnames: A sequence of keyword argument names that have a batch axis.
      in_axes: An integer or sequence of integers indicating the batch axis
        index for each argument in `argnums` and `argnames` should be aligned
        with the list `argnums + argnames`. The default value of 0 assumes
        that all arguments have a batch axis on the 0th dimension of the array.
      num_real_microbatches: Optional number of microbatches that are actually
        executed. If specified, microbatching will terminate early after this
        many steps. Can be helpful to handle variable batch sizes without
        recompilation.

  Returns:
      A new function that evaluates fun sequentially num_microbatches times on
        subsets of data. Consumes the same args and kwargs as ``fun``.
  """
  if microbatch_size is None:
    return fun

  if isinstance(argnums, int):
    argnums = (argnums,)

  if isinstance(argnames, str):
    argnames = (argnames,)

  if isinstance(in_axes, int):
    in_axes = (in_axes,) * (len(argnums) + len(argnames))

  def microbatched_fun(*args, **kwargs):
    reshaped_args, reshaped_kwargs, batch_size = _reshape_all_args(
        microbatch_size, argnums, argnames, in_axes, args, kwargs
    )
    num_microbatches = batch_size // microbatch_size
    accumulator_ = _canonicalize(accumulator, num_microbatches)

    def f(index):
      input_args = list(reshaped_args)
      input_kwargs = dict(reshaped_kwargs)
      for i, ax in zip(argnums, in_axes):
        input_args[i] = jax.tree.map(
            functools.partial(jnp.take, indices=index, axis=ax), input_args[i]
        )
      for i, ax in zip(argnames, in_axes[len(argnums) :]):
        input_kwargs[i] = jax.tree.map(
            functools.partial(jnp.take, indices=index, axis=ax), input_kwargs[i]
        )
      return fun(*input_args, **input_kwargs)

    def body_fun(index, carry):
      return accumulator_.update(carry, f(index), index)

    early_stop = num_real_microbatches is not None
    loop_bound = num_real_microbatches if early_stop else num_microbatches
    init_carry = accumulator_.init(jax.eval_shape(f, 0))
    answer = jax.lax.fori_loop(0, loop_bound, body_fun, init_carry)

    return accumulator_.finalize(answer)

  return microbatched_fun

