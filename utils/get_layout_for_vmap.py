
def get_layout_for_vmap(dim: int, layout: Layout) -> Layout:
  # Make the new dim major-most and shift all other dims by 1 in major_to_minor
  new_m2m = tuple(m + 1 for m in layout.major_to_minor)
  vmapped_major_to_minor = tuple_insert(new_m2m, dim, 0)
  return layout.update(major_to_minor=vmapped_major_to_minor)

