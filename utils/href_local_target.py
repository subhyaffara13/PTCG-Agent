
def href_local_target(el: etree.Element) -> Optional[str]:
    if XLINK_HREF in el.attrib:
        href = el.attrib[XLINK_HREF]
        if href.startswith("#") and len(href) > 1:
            return href[1:]  # drop the leading #
    return None

