from typing import Any, Dict, List

def _build_endpoints(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Transform raw provider_endpoints_support_backup.json into the response shape."""
    providers: Dict[str, Any] = raw.get("providers", {})

    # Collect endpoint keys in insertion order (union across all providers).
    seen: set = set()
    all_keys: List[str] = []
    for provider_data in providers.values():
        for key in provider_data.get("endpoints", {}):
            if key not in seen:
                seen.add(key)
                all_keys.append(key)

    result: List[Dict[str, Any]] = []
    for key in all_keys:
        meta = _ENDPOINT_METADATA.get(key)
        label = meta["label"] if meta else key.replace("_", " ").title()
        path = meta["endpoint"] if meta else "/" + key.replace("_", "/")

        supporting: List[Dict[str, str]] = [
            {
                "slug": slug,
                "display_name": _clean_display_name(pd.get("display_name", slug)),
            }
            for slug, pd in providers.items()
            if pd.get("endpoints", {}).get(key)
        ]
        result.append(
            {"key": key, "label": label, "endpoint": path, "providers": supporting}
        )

    return result

