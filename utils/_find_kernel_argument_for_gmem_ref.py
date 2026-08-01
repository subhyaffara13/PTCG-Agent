
def _find_kernel_argument_for_gmem_ref(gmem_ref: ir.Value) -> ir.Value:
  """Returns the kernel argument value for a given gmem_ref.

  The kernel argument is expected to be an unrealized conversion cast. This
  function will recursively go up block arguments in case of nested blocks.
  """
  if not isinstance(gmem_ref.type, ir.MemRefType):
    raise ValueError(f"Expected {gmem_ref} to have a memref type.")

  while isinstance(gmem_ref, ir.BlockArgument):
    gmem_ref = gmem_ref.owner.owner.operands[gmem_ref.arg_number]

  if ORIGINAL_KERNEL_ARG_ATTR not in gmem_ref.owner.attributes:  # pyrefly: ignore[missing-attribute]
    raise NotImplementedError(
        f"Expected {gmem_ref.owner} to be a GMEM kernel argument."
    )
  return gmem_ref

