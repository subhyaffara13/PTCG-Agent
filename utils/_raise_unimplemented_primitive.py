
def _raise_unimplemented_primitive(primitive):
  if primitive in _densifying_primitives:
    raise NotImplementedError(f"sparse rule for {primitive} is not implemented because it "
                              "would result in dense output. If this is your intent, use "
                              "sparse.todense() to convert your arguments to dense matrices.")
  raise NotImplementedError(f"sparse rule for {primitive} is not implemented.")

