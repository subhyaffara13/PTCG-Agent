from typing import Any

def get_referent(x: Any) -> Any:
  return x.get_referent() if isinstance(x, Tracer) else x

