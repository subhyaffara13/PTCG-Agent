from typing import Any

def add_stack_id_in_entries(
    entries: dict[int, list[dict[str, Any]]],
) -> tuple[dict[int, list[dict[str, Any]]], dict[str, int]]:
    stack_id = 0
    stack_id_trace_map = {}
    for rank in entries:
        for dump in entries[rank]:
            if dump.get("frames", []):
                frames = str(dump["frames"])
                if frames not in stack_id_trace_map:
                    stack_id_trace_map[frames] = stack_id
                    dump["stack_id"] = stack_id
                    stack_id += 1
                else:
                    dump["stack_id"] = stack_id_trace_map[frames]
            else:
                dump["stack_id"] = -1

    return entries, stack_id_trace_map

