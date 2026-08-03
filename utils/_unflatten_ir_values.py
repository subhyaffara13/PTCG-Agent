import math


def _unflatten_ir_values(
    flat_values: Sequence[ir.Value], templates: Sequence[_VectorTemplate | None]
) -> Sequence[ir.Value]:
  """The inverse of ``_flatten_ir_values``."""
  result = []
  flat_values_it = iter(flat_values)
  for template in templates:
    if template is None:
      result.append(next(flat_values_it))
      continue
    registers_shape, layout, vec_type = template
    value_registers = np.asarray(
        [next(flat_values_it) for _ in range(math.prod(registers_shape))],
        dtype=object,
    )
    value = fa.FragmentedArray(
        _registers=value_registers.reshape(registers_shape),
        _layout=layout,
        _is_signed=_default_is_signed(vec_type.element_type),
    )
    result.append(fragmented_array_to_ir(value, vec_type))
  return result

