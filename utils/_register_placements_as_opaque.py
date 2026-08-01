
def _register_placements_as_opaque():
    from torch._library.opaque_object import MemberType, register_opaque_type

    allowed_members = {
        "is_shard": MemberType.USE_REAL,
        "is_partial": MemberType.USE_REAL,
        "is_replicate": MemberType.USE_REAL,
        "__eq__": MemberType.USE_REAL,
    }
    register_opaque_type(Placement, typ="value", members=allowed_members)
    register_opaque_type(
        Shard, typ="value", members=allowed_members | {"dim": MemberType.USE_REAL}
    )
    register_opaque_type(Replicate, typ="value", members=allowed_members)
    register_opaque_type(
        Partial,
        typ="value",
        members=allowed_members | {"reduce_op": MemberType.USE_REAL},
    )
    register_opaque_type(
        _StridedShard,
        typ="value",
        members=allowed_members | {"dim": MemberType.USE_REAL},
    )
    register_opaque_type(
        _MaskPartial,
        typ="value",
        members=allowed_members | {"reduce_op": MemberType.USE_REAL},
    )

