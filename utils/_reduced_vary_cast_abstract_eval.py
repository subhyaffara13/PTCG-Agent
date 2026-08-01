
def _reduced_vary_cast_abstract_eval(aval, *, axes):
  assert isinstance(axes, tuple)
  _check_axis_names(axes, 'reduced_vary_cast')
  if not aval.mat.reduced:
    raise ValueError('reduced_vary_cast only accepts inputs that are'
                     f' reduced. Got {aval.str_short(True)}')
  # If the intersection between aval.mat.reduced and axes is empty, error
  if not (aval.mat.reduced & set(axes)):
    raise ValueError(
        "reduced_vary_cast is a Reduced->Varying collective. This"
        " means that the axis names mentioned in `axes` passed to"
        " `reduced_vary_cast` must be present in"
        f" `jax.typeof(x).mat.reduced`. Got axes={axes} and"
        f" jax.typeof(x).mat.reduced={aval.mat.reduced}")
  if aval.mat.varying & set(axes):
    raise ValueError(
        "reduced_vary_cast input cannot be varying across the axis_name"
        f" provided. Got x={aval.str_short(True)} and axis_name={axes}")

  new_reduced = frozenset(i for i in aval.mat.reduced if i not in axes)
  out_vma = aval.mat.varying | frozenset(axes)
  return aval.update(manual_axis_type=aval.mat.update(
    varying=out_vma, reduced=new_reduced))

