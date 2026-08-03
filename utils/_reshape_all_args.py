from typing import Any

def _reshape_all_args(
    microbatch_size: int,
    argnums: Sequence[int],
    argnames: Sequence[str],
    in_axes: Sequence[int],
    args: tuple[Any, ...],
    kwargs: dict[str, Any]
) -> tuple[tuple[Any, ...], dict[str, Any], int]:
  """Reshapes all batch arguments to have a microbatch axis."""
  new_args = list(args)
  new_kwargs = dict(kwargs)
  batch_args = [args[i] for i in argnums] + [kwargs[i] for i in argnames]

  batch_sizes = jax.tree.flatten(jax.tree.map(
      lambda ax, subtree: jax.tree.map(lambda x: x.shape[ax], subtree),
      tuple(in_axes), tuple(batch_args)
  ))[0]

  if len(set(batch_sizes)) > 1:
    raise ValueError(
        f'Batch Arguments must have equal-size batch axes, found {batch_sizes}.'
    )

  batch_size = list(batch_sizes)[0]
  if batch_size % microbatch_size != 0:
    raise ValueError(f'{batch_size=} must be divisible by {microbatch_size=}.')

  for i, ax in zip(argnums, in_axes):
    new_args[i] = reshape_batch_axis(args[i], microbatch_size, ax)

  for name, ax in zip(argnames, in_axes[len(argnums) :]):
    new_kwargs[name] = reshape_batch_axis(kwargs[name], microbatch_size, ax)

  return tuple(new_args), new_kwargs, tuple(batch_sizes)[0]

