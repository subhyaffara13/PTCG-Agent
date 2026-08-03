import re
from typing import Any

def pp_kv_pair(k:str, v: Any, context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  if type(v) is tuple and all(isinstance(j, (Jaxpr, ClosedJaxpr)) for j in v):
    pp_v = pp_jaxprs(v, context, settings)
  elif isinstance(v, Jaxpr):
    pp_v = pp_jaxpr(v, context, settings)
  elif isinstance(v, ClosedJaxpr):
    pp_v = pp_jaxpr(v.jaxpr, context, settings)
  elif isinstance(v, frozenset):
    pp_v = pp.text(f"frozenset({{{', '.join(repr(e) for e in sorted(v))}}})")
  else:
    s = str(v)
    s = re.sub(
      r' at 0x([0-9a-fA-F]+)', lambda m: ' at 0x' + 'X' * len(m.group(1)), s)
    pp_v = pp.text(s)
  return pp.text(f'{k}=') + pp_v

