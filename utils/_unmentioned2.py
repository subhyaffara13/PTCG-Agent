
def _unmentioned2(mesh: Mesh, spec, manual_axes: frozenset[AxisName]
                  ) -> list[AxisName]:
  # We use a filtered-down version of unmentioned to avoid defensive-psum over
  # more chips than required in the transpose-no-check-vma case.
  name_set = _spec_to_vma(spec) | spec.unreduced
  return [n for n in _all_mesh_names_except_spmd(mesh, manual_axes)
          if n not in name_set]

