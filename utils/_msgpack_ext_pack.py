
def _msgpack_ext_pack(x):
  """Messagepack encoders for custom types."""
  # TODO(flax-dev): Array here only work when they are fully addressable.
  # If they are not fully addressable, use the GDA path for checkpointing.
  if isinstance(x, (np.ndarray, jax.Array)):
    return msgpack.ExtType(_MsgpackExtType.ndarray, _ndarray_to_bytes(x))
  if isinstance(x, np.generic):
    # pack scalar as ndarray
    return msgpack.ExtType(
      _MsgpackExtType.npscalar, _ndarray_to_bytes(np.asarray(x))
    )
  elif isinstance(x, complex):
    return msgpack.ExtType(
      _MsgpackExtType.native_complex, msgpack.packb((x.real, x.imag))
    )
  return x


def _msgpack_ext_pack(x):
  """Messagepack encoders for custom types."""
  # TODO(flax-dev): Array here only work when they are fully addressable.
  # If they are not fully addressable, use the GDA path for checkpointing.
  if isinstance(x, (np.ndarray, jax.Array)):
    return msgpack.ExtType(_MsgpackExtType.NDARRAY, _ndarray_to_bytes(x))
  if issubclass(type(x), np.generic):
    # pack scalar as ndarray
    return msgpack.ExtType(
        _MsgpackExtType.NPSCALAR, _ndarray_to_bytes(np.asarray(x))
    )
  elif isinstance(x, complex):
    return msgpack.ExtType(
        _MsgpackExtType.NATIVE_COMPLEX, msgpack.packb((x.real, x.imag))
    )
  elif isinstance(x, tuple):
    return msgpack.ExtType(
        _MsgpackExtType.TUPLE,
        msgpack.packb(
            list(x),
            strict_types=True,
            use_bin_type=True,
            default=_msgpack_ext_pack,
        ),
    )
  else:
    raise ValueError(f'Unsupported msgpack object: {x}')
  return x

