
def map_inputs(f, *args):
  """Maps over all input BufferedRefs."""
  def fmap(bref, *f_args):
    if bref.is_input:
      return f(bref, *f_args)
    return bref
  return map_brefs(fmap, *args)

