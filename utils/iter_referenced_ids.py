
def iter_referenced_ids(tree: etree.Element) -> Iterator[str]:
    # Yield all the ids that can be reached via references from this element tree.
    # We currently support xlink:href (as used by <use> and gradient templates),
    # and local url(#...) links found in fill or clip-path attributes
    # TODO(anthrotype): Check we aren't missing other supported kinds of reference
    find_svg_elements_with_references = xpath(
        ".//svg:*[ "
        "starts-with(@xlink:href, '#') "
        "or starts-with(@fill, 'url(#') "
        "or starts-with(@clip-path, 'url(#') "
        "or contains(@style, ':url(#') "
        "]",
    )
    for el in chain([tree], find_svg_elements_with_references(tree)):
        ref_id = href_local_target(el)
        if ref_id is not None:
            yield ref_id

        attrs = el.attrib
        if "style" in attrs:
            attrs = {**dict(attrs), **parse_css_declarations(el.attrib["style"])}
        for attr in ("fill", "clip-path"):
            if attr in attrs:
                value = attrs[attr]
                if value.startswith("url(#") and value.endswith(")"):
                    ref_id = value[5:-1]
                    assert ref_id
                    yield ref_id

