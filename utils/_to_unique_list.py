
def _to_unique_list(tags: list[str] | None) -> list[str] | None:
    if tags is None:
        return tags
    unique_tags = []  # make tags unique + keep order explicitly
    for tag in tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    return unique_tags

