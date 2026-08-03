from typing import Any

def _is_observed_module(module: Any) -> bool:
    return hasattr(module, "meta") and "_observed_graph_module_attrs" in module.meta

