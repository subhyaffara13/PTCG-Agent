from typing import List, Optional

def _normalize_images_for_message(
    images: Optional[List[dict]],
) -> Optional[List[ImageURLListItem]]:
    """
    Ensure each image has an 'index' field, as required by ImageURLListItem.
    Some providers (e.g. OpenRouter) return images without index.
    """
    if not images:
        return cast(Optional[List[ImageURLListItem]], images)
    normalized: List[ImageURLListItem] = []
    for i, img in enumerate(images):
        if isinstance(img, dict) and "index" not in img:
            normalized.append(cast(ImageURLListItem, {**img, "index": i}))
        else:
            normalized.append(cast(ImageURLListItem, img))
    return normalized

