
def _vary_unreduced_cast_abstract_eval(aval, *, axes):
  assert isinstance(axes, tuple)
  _check_axis_names(axes, 'vary_unreduced_cast')
  check_unreduced_args([aval], axes, 'vary_unreduced_cast')
  if not aval.mat.varying:
    raise ValueError('vary_unreduced_cast only accepts inputs that are'
                     f' varying. Got {aval.str_short(True)}')
  # If the intersection between aval.mat.varying and axes is empty, error
  if not (aval.mat.varying & set(axes)):
    raise ValueError(
        "vary_unreduced_cast is a Varying->Unreduced collective. This"
        " means that the axis names mentioned in `axes` passed to"
        " `vary_unreduced_cast` must be present in"
        f" `jax.typeof(x).mat.varying`. Got axes={axes} and"
        f" jax.typeof(x).mat.varying={aval.mat.varying}")
  if aval.mat.unreduced & set(axes):
    raise ValueError(
        "vary_unreduced_cast input cannot be unreduced across the axis_name"
        f" provided. Got x={aval.str_short(True)} and axis_name={axes}")

  new_unreduced = aval.mat.unreduced | frozenset(axes)
  out_vma = frozenset(i for i in aval.mat.varying if i not in axes)
  return aval.update(manual_axis_type=aval.mat.update(
    varying=out_vma, unreduced=new_unreduced))

