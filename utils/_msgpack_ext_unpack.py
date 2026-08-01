
def _msgpack_ext_unpack(code, data):
  """Messagepack decoders for custom types."""
  if code == _MsgpackExtType.ndarray:
    return _ndarray_from_bytes(data)
  elif code == _MsgpackExtType.native_complex:
    complex_tuple = msgpack.unpackb(data)
    return complex(complex_tuple[0], complex_tuple[1])
  elif code == _MsgpackExtType.npscalar:
    ar = _ndarray_from_bytes(data)
    return ar[()]  # unpack ndarray to scalar
  return msgpack.ExtType(code, data)


def _msgpack_ext_unpack(code, data):
  """Messagepack decoders for custom types."""
  if code == _MsgpackExtType.NDARRAY:
    return _ndarray_from_bytes(data)
  elif code == _MsgpackExtType.NATIVE_COMPLEX:
    complex_tuple = msgpack.unpackb(data)
    return complex(complex_tuple[0], complex_tuple[1])
  elif code == _MsgpackExtType.NPSCALAR:
    ar = _ndarray_from_bytes(data)
    return ar[()]  # unpack ndarray to scalar
  elif code == _MsgpackExtType.TUPLE:
    return tuple(
        msgpack.unpackb(data, raw=False, ext_hook=_msgpack_ext_unpack)
    )
  else:
    raise ValueError(f'Unsupported msgpack code: {code}')
  return msgpack.ExtType(code, data)

