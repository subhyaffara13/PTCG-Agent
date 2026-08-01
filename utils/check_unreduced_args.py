
def check_unreduced_args(args, axes, name):
  axes = axes if isinstance(axes, (tuple, list)) else (axes,)
  axes = set(axes)
  for a in args:
    if a.mat.unreduced & axes:
      raise ValueError(
          f"{name} cannot accept args which are unreduced. Got"
          f" {a.str_short(True)} and axes={axes}")
    if a.mat.reduced & axes:
      raise ValueError(
          f"{name} cannot accept args which are reduced. Got"
          f" {a.str_short(True)} and axes={axes}")

