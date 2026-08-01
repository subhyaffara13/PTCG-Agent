
def chunk_fragments(fragments: FS, target_shape: Shape) -> FS:
  """Chunks (with zero-copy) the given fragments into the given target shape."""
  new_fragments = []
  for fragment in fragments.fragments:
    new_fragments.extend(chunk_fragment(fragment, target_shape))
  return dataclasses.replace(fragments, fragments=new_fragments)

