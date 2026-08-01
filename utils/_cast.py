
def _cast(value, device_type: str, dtype: _dtype):
    if isinstance(value, torch.Tensor):
        is_eligible = (
            value.is_floating_point()
            and value.device.type == device_type
            and (value.dtype is not torch.float64)
        )
        return value.to(dtype) if is_eligible else value
    elif isinstance(value, (str, bytes)):
        return value
    elif HAS_NUMPY and isinstance(
        value,
        # pyrefly: ignore [missing-attribute]
        np.ndarray,
    ):
        return value
    elif isinstance(value, collections.abc.Mapping):
        return {
            _cast(k, device_type, dtype): _cast(v, device_type, dtype)
            for k, v in value.items()
        }
    elif isinstance(value, collections.abc.Iterable):
        iterable = (_cast(v, device_type, dtype) for v in value)
        if isinstance(value, (list, tuple)):
            return type(value)(iterable)
        else:
            return iterable
    else:
        return value


def _cast(value, device_type: str, dtype: _dtype):
    if isinstance(value, torch.Tensor):
        is_eligible = (
            value.is_floating_point()
            and value.device.type == device_type
            and (value.dtype is not torch.float64)
        )
        return value.to(dtype) if is_eligible else value
    elif isinstance(value, (str, bytes)):
        return value
    elif isinstance(value, collections.abc.Iterable):
        iterable = (_cast(v, device_type, dtype) for v in value)
        if isinstance(value, (list, tuple)):
            return type(value)(iterable)
        else:
            return iterable
    else:
        return value


def _cast(value, dtype):
    return torch.amp.autocast_mode._cast(value, "cuda", dtype)


def _cast(
    src: ir.Value,
    src_type: jax.typing.DTypeLike,
    dst_type: jax.typing.DTypeLike,
    *,
    compute_capability: int | None = None,
) -> ir.Value:
  return _ir_cast(
      src,
      _dtype_to_ir_type(dst_type),
      signed=jnp.issubdtype(src_type, jnp.signedinteger),
      dst_signed=jnp.issubdtype(dst_type, jnp.signedinteger),
      compute_capability=compute_capability,
  )

