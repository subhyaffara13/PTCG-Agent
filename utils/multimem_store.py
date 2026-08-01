
def multimem_store(source: jax.Array, ref: _Ref, collective_axes: Hashable | tuple[Hashable, ...]):
  """Stores the value to ref on all devices present in collective_axes.

  The stores is done using the multimem instructions, meaning that the data is
  only transferred to the switch once, and broadcasted to all other devices
  there.

  Args:
    source: The value to store.
    ref: The GMEM reference to store the value to.
    collective_axes: The JAX mesh axes indicating the devices to store to.
  """
  if isinstance(ref, pallas_core.TransformedRef):
    transforms_leaves, transforms_tree = jax.tree.flatten(
        ref.transforms
    )
    ref = ref.ref
  else:
    transforms_leaves, transforms_tree = [], None
  multimem_store_p.bind(
      source,
      ref,
      *transforms_leaves,
      collective_axes=collective_axes,
      transforms_tree=transforms_tree,
  )


def multimem_store(ptr: ir.Value, value: ir.Value):
  i32 = ir.IntegerType.get_signless(32)
  if (bw := bitwidth(value.type)) not in {32, 64, 128}:
    raise ValueError("Only 32-, 64- and 128-bit stores are supported")
  vector_length = bw // 32
  value = bitcast(value, ir.VectorType.get((vector_length,), i32))
  regs = [
      llvm.extractelement(value, arith.constant(i32, i))
      for i in range(vector_length)
  ]
  if vector_length == 1:
    vec_ptx = "$1"
    vec_mod = ""
  else:
    vec_ptx = f"{{{','.join(f'${i}' for i in range(1, vector_length + 1))}}}"
    vec_mod = ".v" + str(vector_length)
  # It's unclear to me why, but at least according to PTX docs, we have to use
  # the floating-point instructions here to be able to store vectors.
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [ptr, *regs],
      f"multimem.st.relaxed.sys.global{vec_mod}.f32 [$0], {vec_ptx};",
      "l" + ",r" * len(regs),
      has_side_effects=True,
  )

