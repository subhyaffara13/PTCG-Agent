
def sequential_vmap(f):
  """A special case of ``custom_vmap`` that uses a loop.

  A function decorated with ``sequential_vmap`` will be called sequentially
  within a loop when batched. This is useful for functions that don't natively
  support batch dimensions.

  For example:

    >>> @jax.custom_batching.sequential_vmap
    ... def f(x):
    ...   jax.debug.print("{}", x)
    ...   return x + 1
    ...
    >>> jax.vmap(f)(jnp.arange(3))
    0
    1
    2
    Array([1, 2, 3], dtype=int32)

  Where the print statements demonstrate that this :py:func:`~jax.vmap` is being
  generated using a loop.

  See the documentation for :py:class:`~jax.custom_batching.custom_vmap` for
  more details.
  """
  from jax._src.lax import control_flow  # pyrefly: ignore[missing-import]

  f = custom_vmap(f)

  @f.def_vmap
  def rule(axis_size, in_batched, *args):
    del axis_size

    def to_map(mapped_args):
      args = tree_merge(in_batched, mapped_args, bcast_args)
      return f(*args)

    mapped_args, bcast_args = tree_split(in_batched, list(args))
    out = control_flow.map(to_map, mapped_args)
    out_batched = tree_map(lambda _: True, out)
    return out, out_batched

  return f

