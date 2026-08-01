
def _dedupe_tags(tags: List[str]) -> List[str]:
    seen = set()
    deduped_tags = []
    for tag in tags:
        if tag in seen:
            continue
        seen.add(tag)
        deduped_tags.append(tag)
    return deduped_tags

