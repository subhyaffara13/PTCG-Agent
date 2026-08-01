
def validate_fragments_can_be_stacked(fragments: FSconcrete) -> None:
  """Validates that the given fragments can be stacked."""
  if not fragments.fragments:
    raise ValueError('No fragments to stack.')
  fragment_arrays = [
      fragment.value
      for fragment in fragments.fragments
      if fragment.value is not None
  ]
  if len(fragment_arrays) != len(fragments.fragments):
    raise ValueError(f'Not all fragments have values: {fragments}')
  fragment_shape = fragment_arrays[0].shape
  if not all(a.shape == fragment_shape for a in fragment_arrays):
    raise ValueError(
        f"Differently-shaped fragments can't be cast to shards: {fragments}"
    )

