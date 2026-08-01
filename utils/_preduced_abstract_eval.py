
def _preduced_abstract_eval(aval, *, axes):
  assert isinstance(axes, tuple)
  _check_axis_names(axes, 'preduced')
  if aval.mat.varying.intersection(set(axes)):
    raise ValueError(
        "preduced is a Invariant->Reduced collective. This means that the"
        " axis names mentioned in `axes` passed to `preduced` must not be"
        f" present in `jax.typeof(inp).mat.varying`. Got axes={axes} and"
        f" jax.typeof(inp).mat.varying={aval.mat.varying}")
  if aval.mat.reduced & set(axes):
    raise ValueError(
        "preduced input cannot be reduced across the axis_name"
        f" provided. Got x={aval.str_short(True)} and axis_name={axes}")
  return aval.update(manual_axis_type=aval.mat.update(
      reduced=aval.mat.reduced | frozenset(axes)))

