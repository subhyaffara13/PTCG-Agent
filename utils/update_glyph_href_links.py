
def update_glyph_href_links(svg: etree.Element, id_map: Dict[str, str]) -> None:
    # update all xlink:href="#glyph..." attributes to point to the new glyph ids
    for el in xpath(".//svg:*[starts-with(@xlink:href, '#glyph')]")(svg):
        old_id = href_local_target(el)
        assert old_id is not None
        if old_id in id_map:
            new_id = id_map[old_id]
            el.attrib[XLINK_HREF] = f"#{new_id}"

