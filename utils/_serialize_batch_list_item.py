from typing import Any, Dict

def _serialize_batch_list_item(row: Any) -> Dict[str, Any]:
    item: Dict[str, Any] = {}
    file_object = _parse_file_object(row.file_object)
    if isinstance(file_object, dict):
        item.update(file_object)
    item["id"] = row.unified_object_id  # managed ID always wins
    item["object"] = "batch"
    return item

