import json
from typing import Any

def register_namedtuple_serialization(
    nodetype: type[T],
    *,
    serialized_name: str) -> type[T]:
  """Registers a namedtuple for serialization and deserialization.

  JAX has native PyTree support for ``collections.namedtuple``, and does not
  require a call to :func:`jax.tree_util.register_pytree_node`. However, if you
  want to serialize functions that have inputs of outputs of a
  namedtuple type, you must register that type for serialization.

  Args:
    nodetype: the type whose PyTree nodes we want to serialize. It is an
      error to attempt to register multiple serializations for a ``nodetype``.
      On deserialization, this type must have the same set of keys that
      were present during serialization.
    serialized_name: a string that will be present in the serialization and
      will be used to look up the registration during deserialization. It is an
      error to attempt to register multiple serializations for
      a ``serialized_name``.

  Returns:
    the same type passed as ``nodetype``, so that this function can
    be used as a class decorator.
"""
  if not _is_namedtuple(nodetype):
    raise ValueError("Use `jax.export.register_pytree_node_serialization` for "
                     "types other than `collections.namedtuple`.")

  def serialize_auxdata(aux_data: PyTreeAuxData) -> bytes:
    # Store the serialized keys in the serialized auxdata
    del aux_data
    # pyrefly: ignore[missing-attribute]
    return json.dumps(nodetype._fields).encode("utf-8")

  def deserialize_auxdata(serialized_aux_data: bytes) -> PyTreeAuxData:
    return json.loads(serialized_aux_data.decode("utf-8"))

  def from_children(aux_data: PyTreeAuxData, children: Sequence[Any]) -> Any:
    # Use our own "from_children" because namedtuples do not have a pytree
    # registration.
    ser_keys = cast(Sequence[str], aux_data)
    assert len(ser_keys) == len(children)
    return nodetype(** dict(zip(ser_keys, children)))

  return register_pytree_node_serialization(
      nodetype,
      serialized_name=serialized_name,
      serialize_auxdata=serialize_auxdata,
      deserialize_auxdata=deserialize_auxdata,
      from_children=from_children)

