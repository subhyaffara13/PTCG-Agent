
def _get_donated_invars(donate_tuple, in_tree, num_flat_args):
  """Compute donation vector for arguments.

  Args:
    donate_tuple: Tuple of donated argument indices.
    in_tree: PyTreeDef of input structure.
    num_flat_args: Number of flat arguments.

  Returns:
    Tuple of bools indicating which flat args are donated.
  """

  if donate_tuple and not config.debug_nans.value:
    return donation_vector(donate_tuple, (), in_tree)
  else:
    return (False,) * num_flat_args

