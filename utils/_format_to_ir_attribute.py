
def _format_to_ir_attribute(format: PackFormat) -> ir.Attribute:
  return ir.Attribute.parse(f"#tpu.pack_format<{format.value}>")

