import re
from typing import Any

def _generate_stable_operation_id(route: Any) -> str:
    operation_id = re.sub(r"\W", "_", f"{route.name}{route.path_format}")
    route_methods = sorted(route.methods or [])
    if len(route_methods) == 1:
        operation_id = f"{operation_id}_{route_methods[0].lower()}"
    return operation_id

