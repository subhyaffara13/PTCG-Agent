
def _is_shard_like(p: "Placement") -> TypeGuard[Shard | _StridedShard]:
    """Check if a placement is Shard or _StridedShard.

    Use this instead of ``isinstance(p, Shard)`` to avoid silently missing
    ``_StridedShard``.  When ``_StridedShard`` is unified with ``Shard``
    (see TODO on the class), this helper can be collapsed to a single
    ``isinstance`` check.
    """
    return isinstance(p, Shard | _StridedShard)

