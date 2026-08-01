
def free_ref(ref: Ref):
  """Invalidate a given reference."""
  free_ref_p.bind(ref)
  return ()

