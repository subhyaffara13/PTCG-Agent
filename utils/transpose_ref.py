
def transpose_ref(
    ref: pallas_core.TransformedRef | Any,
    permutation: tuple[int, ...],
) -> pallas_core.TransformedRef:
  assert hasattr(ref, "memory_space")
  if ref.memory_space == MemorySpace.TMEM:
    raise ValueError("Can't transpose a TMEM reference.")
  return ref.transpose(permutation)

