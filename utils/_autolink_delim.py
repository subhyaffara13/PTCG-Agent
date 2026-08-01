
def _autolink_delim(data: str, link_end: int) -> int:
    """Trim trailing punctuation from a URL according to GFM rules."""
    # Truncate at first '<'
    for i, ch in enumerate(data[:link_end]):
        if ch == "<":
            link_end = i
            break

    while link_end > 0:
        cclose = data[link_end - 1]

        copen = "(" if cclose == ")" else None

        if cclose in _LINK_END_ASSORTMENT:
            link_end -= 1
        elif cclose == ";":
            new_end = link_end - 2
            while new_end > 0 and data[new_end].isalpha():
                new_end -= 1
            if new_end < link_end - 2 and data[new_end] == "&":
                link_end = new_end
            else:
                link_end -= 1
        elif copen is not None:
            opening = data[:link_end].count(copen)
            closing = data[:link_end].count(cclose)
            if closing <= opening:
                break
            link_end -= 1
        else:
            break

    return link_end

