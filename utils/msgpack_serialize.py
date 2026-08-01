
def msgpack_serialize(pytree, in_place: bool = False) -> bytes:
  """Save data structure to bytes in msgpack format.

  Low-level function that only supports python trees with array leaves,
  for custom objects use ``to_bytes``.  It splits arrays above MAX_CHUNK_SIZE into
  multiple chunks.

  Args:
    pytree: python tree of dict, list, tuple with python primitives
      and array leaves.
    in_place: boolean specifying if pytree should be modified in place.

  Returns:
    msgpack-encoded bytes of pytree.
  """
  if not in_place:
    pytree = jax.tree_util.tree_map(lambda x: x, pytree)
  pytree = _np_convert_in_place(pytree)
  pytree = _chunk_array_leaves_in_place(pytree)
  return msgpack.packb(pytree, default=_msgpack_ext_pack, strict_types=True)


def msgpack_serialize(pytree, in_place: bool = False) -> bytes:
  """Save data structure to bytes in msgpack format.

  Low-level function that only supports python trees with array leaves,
  for custom objects use `to_bytes`.  It splits arrays above MAX_CHUNK_SIZE into
  multiple chunks.

  Args:
    pytree: python tree of dict, list, tuple with python primitives
      and array leaves.
    in_place: boolean specifyng if pytree should be modified in place.

  Returns:
    msgpack-encoded bytes of pytree.
  """
  if not in_place:
    pytree = jax.tree.map(lambda x: x, pytree)
  pytree = _np_convert_in_place(pytree)
  pytree = _chunk_array_leaves_in_place(pytree)
  return msgpack.packb(pytree, default=_msgpack_ext_pack, strict_types=True)

