
def save_and_offload_only_these_names(
    *, names_which_can_be_saved, names_which_can_be_offloaded,
    offload_src, offload_dst):
  """Same as ``save_only_these_names``, but offload to CPU memory instead of
  recomputing."""
  names_which_can_be_saved = set(names_which_can_be_saved)
  names_which_can_be_offloaded = set(names_which_can_be_offloaded)
  intersection = names_which_can_be_saved.intersection(names_which_can_be_offloaded)
  if intersection:
    raise ValueError(
        "The names should be exclusive and should not intersect in"
        " `names_which_can_be_saved` and `names_which_can_be_offloaded`. Got"
        f" names_which_can_be_saved={names_which_can_be_saved},"
        f" names_which_can_be_offloaded={names_which_can_be_offloaded} and the"
        f" intersection={intersection}")
  def policy(prim, *_, **params):
    if prim is name_p and params['name'] in names_which_can_be_saved:
      return pe.Saveable
    if prim is name_p and params['name'] in names_which_can_be_offloaded:
      return pe.Offloadable(src=offload_src, dst=offload_dst)
    return pe.Recompute  # not saveable unless it's in the allow-list
  return policy

