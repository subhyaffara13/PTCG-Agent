from typing import Any, Dict, Tuple

def parse_cluster_slots(
    resp: Any, **options: Any
) -> Dict[Tuple[int, int], Dict[str, Any]]:
    current_host = options.get("current_host", "")

    def fix_server(*args: Any) -> Tuple[str, Any]:
        return str_if_bytes(args[0]) or current_host, args[1]

    slots = {}
    for slot in resp:
        start, end, primary = slot[:3]
        replicas = slot[3:]
        slots[start, end] = {
            "primary": fix_server(*primary),
            "replicas": [fix_server(*replica) for replica in replicas],
        }

    return slots

