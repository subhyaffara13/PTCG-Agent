
def _register_distributed_opaque_types():
    """
    Register DeviceMesh as an opaque type for torch.compile.
    This must happen before any custom ops that use DeviceMesh in their schema.
    Called lazily to avoid circular import issues.
    """
    global _distributed_opaque_types_registered
    if _distributed_opaque_types_registered:
        return
    _distributed_opaque_types_registered = True

    from torch._library.opaque_object import MemberType, register_opaque_type

    register_opaque_type(
        ProcessGroup,
        typ="reference",
        members={
            "size": MemberType.USE_REAL,
            "rank": MemberType.USE_REAL,
            "_get_backend_name": MemberType.USE_REAL,
            "group_name": MemberType.USE_REAL,
            "group_desc": MemberType.USE_REAL,
            "__eq__": MemberType.USE_REAL,
            "__ne__": MemberType.USE_REAL,
        },
    )

    register_opaque_type(
        DeviceMesh,
        typ="reference",
        reconstruct_fn=_device_mesh_reconstruct_fn,
        guard_fn=lambda obj: [
            obj._flatten_rank_map,
            obj._layout,
            obj._device_type,
            obj._mesh_dim_names,
            obj._thread_id,
        ],
        members={
            # USE_REAL: Evaluate these with the real object at compile time
            # and bake the result as a constant
            "_flatten_rank_map": MemberType.USE_REAL,
            "_layout": MemberType.USE_REAL,
            "_device_type": MemberType.USE_REAL,
            "_mesh_dim_names": MemberType.USE_REAL,
            "_thread_id": MemberType.USE_REAL,
            "get_rank": MemberType.USE_REAL,
            "size": MemberType.USE_REAL,
            "get_coordinate": MemberType.USE_REAL,
            "get_local_rank": MemberType.USE_REAL,
            "__eq__": MemberType.USE_REAL,
            "__ne__": MemberType.USE_REAL,
            "ndim": MemberType.USE_REAL,
            "shape": MemberType.USE_REAL,
            "mesh_dim_names": MemberType.USE_REAL,
            "get_group": MemberType.INLINED,
            "_pg_registry": MemberType.INLINED,
            "_hash": MemberType.USE_REAL,
            "_create_flatten_mesh": MemberType.USE_REAL,
            "_coordinate_on_dim": MemberType.USE_REAL,
            "_dim_group_names": MemberType.USE_REAL,
            "_flatten_mapping": MemberType.USE_REAL,
            "_rank_map": MemberType.USE_REAL,
            "_root_mesh": MemberType.USE_REAL,
            "device_type": MemberType.USE_REAL,
            "mesh": MemberType.USE_REAL,
            "_flatten": MemberType.INLINED,
            "_unflatten": MemberType.USE_REAL,
            "_is_current_rank_part_of_mesh": MemberType.USE_REAL,
            "_sym_get_coordinate": MemberType.USE_REAL,
            "_get_mesh_dim_by_name": MemberType.USE_REAL,
            "_get_root_mesh": MemberType.INLINED,
            "__getitem__": MemberType.INLINED,
            "_get_slice_mesh_layout": MemberType.INLINED,
            "_create_sub_mesh": MemberType.INLINED,
        },
    )

