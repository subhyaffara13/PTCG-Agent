
def _record_to_dict(record: Any) -> Dict[str, Any]:
    if isinstance(record, dict):
        return record
    if hasattr(record, "model_dump") and callable(record.model_dump):
        return record.model_dump()
    if hasattr(record, "dict") and callable(record.dict):
        return record.dict()
    return dict(record)

