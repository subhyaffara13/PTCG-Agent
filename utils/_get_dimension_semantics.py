
def _get_dimension_semantics(
    dimension_semantics: Sequence[str],
) -> ir.ArrayAttr:

  def _get_semantics(s: str | None) -> str:
    if s is None:
      return "#tpu.dimension_semantics<arbitrary>"
    return f"#tpu.dimension_semantics<{s}>"

  return ir.ArrayAttr.get(
      map(
          ir.Attribute.parse,
          map(_get_semantics, dimension_semantics),
      )
  )

