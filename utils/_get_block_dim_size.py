
def _get_block_dim_size(dim: BlockDim) -> int:
  match dim:
    case Squeezed():
      return 1
    case (
        Blocked(block_size)
        | Element(block_size)
        | BoundedSlice(block_size)
        | Indirect(block_size)
    ):
      return block_size
    case _:
      raise ValueError(f"Unsupported block shape type: {type(dim)}")

