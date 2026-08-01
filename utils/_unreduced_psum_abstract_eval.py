
def _unreduced_psum_abstract_eval(aval, *, axes):
  _check_axis_names(axes, 'psum')
  if not aval.mat.unreduced:
    raise ValueError('unreduced_psum only accepts inputs that are'
                      f' unreduced. Got {aval.str_short(True)}')
  # If intersection between x.unreduced & axis_name is empty, error
  if not (aval.mat.unreduced & frozenset(axes)):
    raise ValueError(
        "unreduced_psum is a Unreduced -> Invariant collective. This"
        f" means that the {axes=} passed to `unreduced_psum` must"
        " be present in"
        f" jax.typeof(x).mat.unreduced={aval.mat.unreduced}")
  if aval.mat.varying & set(axes):
    raise ValueError(
        "unreduced_psum's input cannot be varying across the "
        f" axis_name provided. Got x={aval.str_short(True)} and {axes=}")

  if any(isinstance(a, int) for a in axes):
    raise ValueError('unreduced_psum does not accept integer axis_name.'
                     f' Got axis_name={axes}')

  core.check_avals_context_mesh([aval], 'unreduced_psum')
  out_mat = aval.mat.update(unreduced=frozenset(u for u in aval.mat.unreduced
                                                if u not in axes))
  out_aval = aval.update(manual_axis_type=out_mat)
  return out_aval, {core.NamedAxisEffect(axis) for axis in axes}

