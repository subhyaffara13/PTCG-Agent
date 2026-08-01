
def _spec_to_mat(spec) -> core.ManualAxisType:
  return core.ManualAxisType(varying=_spec_to_vma(spec),
                             unreduced=spec.unreduced, reduced=spec.reduced)

