
def _canonicalize_block_dim(dim: BlockDim | int | None) -> BlockDim:
  match dim:
    case None:
      return squeezed
    case int():
      return Blocked(int(dim))
    case Squeezed() | Blocked() | Element() | BoundedSlice() | Indirect():
      return dim
    case _:
      # Handle case where the dim is a symbolic dimension so we assume it is
      # Blocked.
      if jax_core.is_symbolic_dim(dim):
        return Blocked(dim)
      try:
        return Blocked(int(dim))
      except Exception as e:
        raise ValueError(
            f"Unsupported block dimension type: {type(dim)}. Allowed types:"
            " `pl.Squeezed`, `pl.Blocked`, `pl.Element`, `int`, `None`."
        ) from e

