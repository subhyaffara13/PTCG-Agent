
def _block_size(dim: pallas_core.Element | int | None) -> int | None:
  match dim:
    case (
        pallas_core.Element()
        | pallas_core.BoundedSlice()
        | pallas_core.Blocked()
    ):
      return dim.block_size
    case pallas_core.Squeezed() | None:
      return None
    case _:
      return dim

