
def closure_element_ids(
    elements: Dict[str, etree.Element], element_ids: Set[str]
) -> None:
    # Expand the initial subset of element ids to include ids that can be reached
    # via references from the initial set.
    unvisited = element_ids
    while unvisited:
        referenced: Set[str] = set()
        for el_id in unvisited:
            if el_id not in elements:
                # ignore dangling reference; not our job to validate svg
                continue
            referenced.update(iter_referenced_ids(elements[el_id]))
        referenced -= element_ids
        element_ids.update(referenced)
        unvisited = referenced

