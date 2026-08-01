
def unique_slug(slug: str, slugs: set[str]) -> str:
    uniq = slug
    i = 1
    while uniq in slugs:
        uniq = f"{slug}-{i}"
        i += 1
    slugs.add(uniq)
    return uniq

