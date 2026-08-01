
def stack_fragments(fragments: FSconcrete | None) -> Aconcrete | None:
  """Stacks the given fragments, which must all have the same shape."""
  if fragments is None:
    return fragments
  validate_fragments_can_be_stacked(fragments)
  fragment_arrays = [fragment.value for fragment in fragments.fragments]
  np_api = fragments.FRAGMENT_T.NP_API
  return (
      np_api.expand_dims(fragment_arrays[0], axis=0)
      if len(fragment_arrays) == 1
      else np_api.stack(fragment_arrays)
  )

