
def get_pytree_SUPPORTED_NODES_source() -> AttrSource:
    return AttrSource(
        AttrSource(AttrSource(ImportSource("torch"), "utils"), "_pytree"),
        "SUPPORTED_NODES",
    )

