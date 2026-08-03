from typing import Any

def _dict_attribute_handler(val: dict[str, Any]) -> ir.Attribute:
  return ir.DictAttr.get({k: ir_attribute(v) for k, v in val.items()})

