
def _select_shape_rule(which, *cases):
  if len(cases) == 0:
    raise TypeError("select must have at least one case")
  if any(case.shape != cases[0].shape for case in cases[1:]):
    msg = "select cases must have the same shapes, got [{}]."
    raise TypeError(msg.format(", ".join([str(c.shape) for c in cases])))
  if which.shape and which.shape != cases[0].shape:
    msg = ("select `which` must be scalar or have the same shape as cases, "
           "got `which` shape {} but case shape {}.")
    raise TypeError(msg.format(which.shape, cases[0].shape))
  return cases[0].shape

