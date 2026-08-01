
def map_outputs(f, *args):
  """Maps over all output BufferedRefs."""
  def fmap(bref, *f_args):
    if bref.is_output:
      return f(bref, *f_args)
    return bref
  return map_brefs(fmap, *args)

