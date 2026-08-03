from typing import Any

def deserialize_pytreedef(pytreedef_repr: dict[str, Any]):
  buf = base64.b64decode(pytreedef_repr[_TREE_REPR_KEY])
  exp = ser_flatbuf.PyTreeDef.GetRootAs(buf)
  treestruct = _deserialize_pytreedef(exp)
  return treestruct

