
def fetch_and_add(
    x_ref: jax.Ref | state_types.TransformedRef,
    value: jax.typing.ArrayLike,
    *,
    subcore_id: jax.typing.ArrayLike,
) -> jax.Array:
  """Adds value to the ``x_ref`` on another subcore.

  Be careful to ensure subcores are synchronized between initializing the SMEM
  (on the target subcore) and adding to it, potentially using
  ``plsc.subcore_barrier()``.

  Args:
    x_ref: A scalar SMEM ref.
    value: The value to add to ``x_ref`` on ``subcore_id``.
    subcore_id: The ID of the vector subcore to use.

  Returns:
    The value of ``x_ref`` on the specified subcore before adding ``value``.
  """
  if x_ref.size != 1:
    raise ValueError(f"Expected a scalar ref, but got {x_ref.shape=}.")

  x_ref, transforms = pallas_primitives._get_ref_and_transforms(x_ref)
  match transforms:
    case []:
      indices = [jnp.int32(0)] * x_ref.ndim
    case [indexing.NDIndexer(indices=indices) as indexer]:
      if any(isinstance(i, indexing.Slice) for i in indexer.indices):
        raise ValueError(
            "fetch_and_add only supports refs indexed with non-slice indices,"
            f" but got {indices}"
        )
    case _:
      raise ValueError(
          "fetch_and_add requires a scalar ref with a single non-slice"
          f" indexer, but got {transforms}"
      )
  return fetch_and_add_p.bind(x_ref, value, *indices, subcore_id)

