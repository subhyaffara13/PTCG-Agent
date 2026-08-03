from typing import Any

def _attach_xla_metadata_to_op(
    xla_metadata: dict[str, Any], op: ir.Operation
) -> None:
  if xla_metadata:
    ctx_attributes, existing_attributes = {}, {}
    for k, v in xla_metadata.items():
      v_str = str(v).lower() if isinstance(v, bool) else str(v)
      ctx_attributes[k] = ir.StringAttr.get(v_str)
    # Combine with existing mhlo.frontend_attributes
    for attr in op.attributes:
      if attr == "mhlo.frontend_attributes":
        for a in ir.DictAttr(op.attributes[attr]):
          existing_attributes[a.name] = a.attr
    op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(
        ctx_attributes | existing_attributes
    )

