
def target_blank(attrs, new=False):
    href_key = (None, "href")

    if href_key not in attrs:
        return attrs

    if attrs[href_key].startswith("mailto:"):
        return attrs

    attrs[(None, "target")] = "_blank"
    return attrs

