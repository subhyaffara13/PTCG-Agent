
def compute_local_shape_and_global_offset(
    global_shape: ShapeType,
    mesh: DeviceMesh,
    placements: Sequence[Placement],
    skip_offset: bool = False,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """
    Compute the local tensor shape and the global offsets into the original tensor
    of a DTensor on its current global rank. This is useful for checkpointing purpose.

    Example:
    global_tensor = [[0,  1,  2,  3,  4], sharded on mesh (DP=2, TP=2) with (Shard(1), Shard(1))
                     [10, 11, 12, 13, 14]]

    This table shows the return value of local_shape and global_offset for each rank.
    (`local_tensor` is for illustration only).

    Note how the first coordinate of global_offset is always 0, corresponding to tensor dim 0 being replicated.

    Rank        local_tensor        local_shape     global_offset
    -------------------------------------------------------------
    0           [[0, 1],            (2, 2)          (0, 0)
                 [10, 11]]

    1           [[2],               (2, 1)          (0, 2)
                 [12]]

    2           [[3],               (2, 1)          (0, 3)
                 [13]]

    3           [[4],               (2, 1)          (0, 4)
                 [14]]

    Args:
        global_shape (ShapeType): The global shape of the DTensor.
        mesh (:class:`DeviceMesh`): The device mesh this DTensor is distributed on.
        placements (Sequence[:class:`Placement`]]): The placements of the DTensor.
        skip_offset (bool): If True, skip computing the global offsets and return an empty
            tuple for global_offset. This can improve performance when only the local shape
            is needed. Defaults to False.

    Return:
        local_shape: the shape of the DTensor's _local_tensor on the current rank.
        global_offset: a tuple of offsets for each dimension of the global tensor shape,
        identifying how this shard fits into the global tensor in each dimension. If
        skip_offset is True, this will be an empty tuple.

    """
    empty_offset = ()
    if not mesh._is_current_rank_part_of_mesh():
        # if rank not in the mesh, return empty offset
        return ((0,), empty_offset)

    return _compute_local_shape_and_global_offset(
        global_shape, mesh.shape, mesh._sym_get_coordinate, placements, skip_offset
    )

