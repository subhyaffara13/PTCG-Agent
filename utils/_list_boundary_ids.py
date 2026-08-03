from typing import Any, List, Optional, Tuple

def _list_boundary_ids(
    rows: List[Any], resource_kind: str
) -> Tuple[Optional[str], Optional[str]]:
    if not rows:
        return None, None
    id_attr = "unified_file_id" if resource_kind == "files" else "unified_object_id"
    return getattr(rows[0], id_attr), getattr(rows[-1], id_attr)

