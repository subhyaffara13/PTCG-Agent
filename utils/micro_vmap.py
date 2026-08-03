from typing import Any

def micro_vmap(
    fun: Function,
    in_axes: int | Sequence[int] = 0,
    out_axes: Any = 0,
    *,
    microbatch_size: int | None = None,
    vmap_fn: VmapFn = jax.vmap,
    accumulator: (
        Accumulator | AccumulationType | AccumulatorTree
    ) = AccumulationType.CONCAT,
    num_real_microbatches: int | jax.Array | None = None,
) -> Function:
  """A generalized version of jax.vmap that supports microbatching.

  Because this function incorporates microbatching, you can vmap over
  arrays with much larger batch axis sizes than jax.vmap without running
  out of memory. This function generalizes vmap by introducing new keyword
  arguments `microbatch_size` and `accumulator` to control microbatching
  behavior. It specializes vmap by imposing stricter requirements on `in_axes`
  and `out_axes`.

  Example Usage:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> optax.microbatching.micro_vmap(lambda x: x**2)(jnp.arange(8))
    Array([ 0,  1,  4,  9, 16, 25, 36, 49], dtype=int32)

  Args:
    fun: Function to be mapped over additional axes.
    in_axes: Array axis to map over.  See jax.vmap for more details.
    out_axes: Unsupported by optax.vmap, must be set to 0.
    microbatch_size: The number of rows in the overall batch used in each
      microbatch. Smaller values reduces memory overhead, but require more
      sequential computation. This must evenly divide the batch axis size of
      the batch arguments.
    vmap_fn: A function with the same signature as jax.vmap.  Can be used to
      e.g., pass in kwargs to vmap.
    accumulator: Specifies what to do with the vmapped outputs.  The default
      value (CONCAT) returns each output with a batch axis, matching the
      behavior of jax.vmap. Reductions over the batch axis are also possible,
      including MEAN and SUM, and can be used when the the full output with a
      batch axis is not needed and is too large to fit in memory. This
      accumulator can be any PyTree prefix of the outputs of `fun` to apply
      different reductions to different sub-trees.
    num_real_microbatches: Optional number of microbatches that are actually
      executed. If specified, microbatching will terminate early after this
      many steps. Can be helpful to handle variable batch sizes without
      recompilation.

  Returns:
    A new function with the same args and kwargs having an additional
    batch axis (according to in_axes).
  """

  if out_axes != 0:
    raise NotImplementedError('out_axis != 0 is not currently supported')

  if isinstance(in_axes, int):
    in_axes = (in_axes,)

  # The semantics of vmap require that all kwargs are mapped along the leading
  # axis. We therefore bundle all kwargs into a single dictionary kwarg below.
  def vmap_reduce_fn(*args, kwargs):
    output = vmap_fn(fun, in_axes, out_axes)(*args, **kwargs)
    microbatch_size_ = jax.tree.leaves(output)[0].shape[0]

    # We are only relying on the `aggregate` attribute of the accumulator, which
    # does not require knowledge of the number of microbatches.
    temporary_accumulator = _canonicalize(accumulator, microbatch_size_)
    return temporary_accumulator.aggregate(output)

  micro_vmap_fn = microbatch(
      vmap_reduce_fn,
      argnums=tuple(x[0] for x in enumerate(in_axes) if x[1] is not None),
      argnames='kwargs',
      microbatch_size=microbatch_size,
      accumulator=accumulator,
      in_axes=tuple(ax for ax in in_axes if ax is not None) + (0,),
      num_real_microbatches=num_real_microbatches,
  )

  def wrapped_fn(*args, **kwargs):
    return micro_vmap_fn(*args, kwargs=kwargs)

  return wrapped_fn

