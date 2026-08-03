from typing import Any, Dict

def _pack_config_row(row: Any) -> Dict[str, Any]:
    return {"param_name": row.param_name, "param_value": row.param_value}

