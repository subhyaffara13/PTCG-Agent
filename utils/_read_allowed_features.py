from typing import Any, Dict

def _read_allowed_features(license_data: Dict[str, Any]) -> list:
    raw_allowed_features = license_data.get("allowed_features")
    if isinstance(raw_allowed_features, list):
        return list(raw_allowed_features)
    if raw_allowed_features is None:
        return []
    return [raw_allowed_features]

