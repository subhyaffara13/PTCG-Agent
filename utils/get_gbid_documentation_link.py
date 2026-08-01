
def get_gbid_documentation_link(gb_type: str) -> str | None:
    """
    Retrieves the GBID documentation link for a given graph break type.

    Args:
        gb_type: The graph break type to look up.

    Returns:
        A string containing the documentation URL if found, otherwise None.
    """
    GRAPH_BREAK_SITE_URL = (
        "https://meta-pytorch.github.io/compile-graph-break-site/gb/"  # @lint-ignore
    )

    gb_type_to_gb_id_map = _load_gb_type_to_gb_id_map()

    if gb_type in gb_type_to_gb_id_map:
        return (
            f"{GRAPH_BREAK_SITE_URL}gb{gb_type_to_gb_id_map[gb_type].lstrip('GB')}.html"
        )

    return None

