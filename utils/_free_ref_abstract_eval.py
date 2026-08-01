
def _free_ref_abstract_eval(ref_aval):
  # No effects, but there is a custom DCE rule that prevents free_ref from
  # being DCE'd.
  return (), {}

