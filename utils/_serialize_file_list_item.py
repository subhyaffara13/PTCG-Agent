from typing import Any, Dict

def _serialize_file_list_item(row: Any) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "id": row.unified_file_id,
        "object": "file",
        "created_at": int(row.created_at.timestamp()) if row.created_at else None,
    }
    file_object = _parse_file_object(row.file_object)
    if isinstance(file_object, dict):
        item.update(file_object)
    item["id"] = row.unified_file_id  # managed ID always wins over stored raw id
    return item

