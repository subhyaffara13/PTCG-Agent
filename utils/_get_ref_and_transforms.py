
def _get_ref_and_transforms(ref):
  if isinstance(ref, state.TransformedRef):
    return ref.ref, ref.transforms
  return ref, ()


def _get_ref_and_transforms(ref):
  if isinstance(ref, state.TransformedRef):
    return ref.ref, ref.transforms
  return ref, ()

