
def _update_frontend_attributes(op, attrs):
  if isinstance(op, ir.Block):
    return
  if attr_array := op.attributes.get("mhlo.frontend_attributes"):
    assert isinstance(attr_array, ir.DictAttr)
    attrs |= {a.name: a.attr for a in attr_array}
  op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(attrs)

