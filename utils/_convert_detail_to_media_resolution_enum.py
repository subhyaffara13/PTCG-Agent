
def _convert_detail_to_media_resolution_enum(
    detail: Optional[str],
) -> Optional[Dict[str, str]]:
    if detail == "low":
        return {"level": "MEDIA_RESOLUTION_LOW"}
    elif detail == "medium":
        return {"level": "MEDIA_RESOLUTION_MEDIUM"}
    elif detail == "high":
        return {"level": "MEDIA_RESOLUTION_HIGH"}
    elif detail == "ultra_high":
        return {"level": "MEDIA_RESOLUTION_ULTRA_HIGH"}
    return None

