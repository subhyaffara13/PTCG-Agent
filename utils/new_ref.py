
def new_ref(init_val: Any, *, memory_space: Any = None, kind: Any = None):
  """Create a mutable array reference with initial value ``init_val``.

  For more discussion, see the `Ref guide`_.

  Args:
    init_val: A :class:`jax.Array` representing the initial state
      of the buffer.
    memory_space: An optional memory space attribute for the Ref.
    kind: An optional string indicating the mutation semantics under
      rematerialization.

  Returns:
    A :class:`jax.ref.Ref` containing a reference to a mutable buffer.

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  return ref_p.bind(init_val, memory_space=memory_space, kind=kind)


def new_ref(
    init_val: Any, *, memory_space: Any = None, kind: str | None = None
) -> core.Ref:
  """Create a mutable array reference with initial value ``init_val``.

  For more discussion, see the `Ref guide`_.

  Args:
    init_val: A :class:`jax.Array` representing the initial state
      of the buffer.
    memory_space: An optional memory space attribute for the Ref.
    kind: An optional string indicating the mutation semantics under
      rematerialization. Currently only supports ``'no_grad_no_remat'`` or
      ``None``.

  Returns:
    A :class:`jax.ref.Ref` containing a reference to a mutable buffer.

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  return core.new_ref(init_val, memory_space=memory_space, kind=kind)

