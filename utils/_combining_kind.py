
def _combining_kind(attr: ir.Attribute) -> vector.CombiningKind:
  return vector.CombiningKind[
      str(attr).removeprefix("#vector.kind<").removesuffix(">").upper()
  ]

