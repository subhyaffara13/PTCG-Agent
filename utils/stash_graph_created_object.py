from typing import Any

def stash_graph_created_object(obj: Any) -> Any:
    keep_alive.append(obj)
    return obj

