from typing import Any

def is_visibility_more_specific(
    candidate: FixtureDef[Any], other: FixtureDef[Any]
) -> bool:
    """Return whether the visibility of ``candidate`` is strictly more specific
    than that of ``other``, i.e. ``candidate`` is defined on a strict descendant
    in the collection tree of where ``other`` is defined."""
    if candidate.node is None or other.node is None:
        # Fallback for fixtures registered with a string nodeid (deprecated).
        # In this case compare baseids, which are nodeid prefixes.
        # This branch can be removed once baseid deprecation is done (pytest 10).
        if candidate.baseid == other.baseid:
            return False
        if other.baseid == "":
            return True
        # `candidate.baseid` must continue with a node separator for it to be a
        # true descendant.
        return candidate.baseid.startswith(other.baseid) and candidate.baseid[
            len(other.baseid)
        ] in ("/", ":")

    return (
        candidate.node is not other.node and other.node in candidate.node.iter_parents()
    )

