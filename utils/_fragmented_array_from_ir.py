import math


def _fragmented_array_from_ir(
    fragmented_array_as_ir: ir.Value,
    layout: ir.Attribute,
    is_signed: bool | None = None,
) -> fa.FragmentedArray:
  producer_layout_attr = fragmented_array_as_ir.owner.attributes["layout"]  # pyrefly: ignore[missing-attribute]
  producer_layout = layouts_lib.from_layout_attr(producer_layout_attr)
  vector_ty = ir.VectorType(fragmented_array_as_ir.type)
  reg_shape = producer_layout.registers_shape(tuple(vector_ty.shape))
  reg_ty: ir.Type = producer_layout.registers_element_type(vector_ty.element_type)

  conversion_cast, converted_outputs = _undo_conversion_cast(
      fragmented_array_as_ir, [reg_ty] * math.prod(reg_shape)
  )

  reverse_conversion_cast = converted_outputs[0].owner.opview  # pyrefly: ignore[missing-attribute]
  for attribute in conversion_cast.attributes:
    reverse_conversion_cast.attributes[attribute] = conversion_cast.attributes[attribute]

  registers = np.array(list(converted_outputs)).reshape(
    [
        attr.value  # pyrefly: ignore[missing-attribute]
        for attr in ir.ArrayAttr(conversion_cast.attributes["registers_shape"])
    ]
  )

  if isinstance(conversion_cast.outputs[0].type.element_type, ir.IntegerType):
    is_signed = False if is_signed is None else is_signed

  return fa.FragmentedArray(
      _registers=registers, _layout=producer_layout, _is_signed=is_signed
  ).to_layout(layouts_lib.from_layout_attr(layout))

