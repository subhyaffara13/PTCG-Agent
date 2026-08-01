
def msgpack_restore(encoded_pytree: bytes):
  """Restore data structure from bytes in msgpack format.

  Low-level function that only supports python trees with array leaves,
  for custom objects use ``from_bytes``.

  Args:
    encoded_pytree: msgpack-encoded bytes of python tree.

  Returns:
    Python tree of dict, list, tuple with python primitive
    and array leaves.
  """
  state_dict = msgpack.unpackb(
    encoded_pytree, ext_hook=_msgpack_ext_unpack, raw=False
  )
  return _unchunk_array_leaves_in_place(state_dict)


def msgpack_restore(encoded_pytree: bytes):
  """Restore data structure from bytes in msgpack format.

  Low-level function that only supports python trees with array leaves,
  for custom objects use `from_bytes`.

  Args:
    encoded_pytree: msgpack-encoded bytes of python tree.

  Returns:
    Python tree of dict, list, tuple with python primitive
    and array leaves.
  """
  state_dict = msgpack.unpackb(
      encoded_pytree, ext_hook=_msgpack_ext_unpack, raw=False)
  return _unchunk_array_leaves_in_place(state_dict)

