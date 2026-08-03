from typing import Any

def _default_res_aval_updater(
    params: dict[str, Any], aval: AbstractValue) -> AbstractValue:
  return aval

