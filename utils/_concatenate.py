
def _concatenate(
    tensors, axis=0, out=None, dtype=None, casting: CastingModes | None = "same_kind"
):
    # pure torch implementation, used below and in cov/corrcoef below
    tensors, axis = _util.axis_none_flatten(*tensors, axis=axis)
    tensors = _concat_cast_helper(tensors, out, dtype, casting)
    return torch.cat(tensors, axis)


def _concatenate(a: Array, b: Array) -> Array:
  """Concatenates two arrays along the last dimension."""
  return jnp.concatenate([a, b], axis=-1)


def _concatenate(a: Array, b: Array) -> Array:
    """Concatenates two arrays along the last dimension."""
    return jnp.concatenate([a, b], axis=-1)

