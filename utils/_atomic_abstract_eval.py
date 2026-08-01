
def _atomic_abstract_eval(*avals_flat, args_tree, atomic_type: AtomicOpType):
  ref, _, _, _ = args_tree.unflatten(avals_flat)
  if ref.dtype == jnp.dtype("float16") and atomic_type != AtomicOpType.ADD:
    raise ValueError(f"`atomic_{atomic_type.value}` does not support f16.")
  if ref.dtype in {
      jnp.dtype("bool"),
      jnp.dtype("int8"),
      jnp.dtype("int16"),
      jnp.bfloat16,
  }:
    raise ValueError(
        f"`atomic_{atomic_type.value}` does not support {ref.dtype}."
    )
  return pallas_primitives._swap_abstract_eval(*avals_flat, args_tree=args_tree)

