
def compute_global_tensor_shape(
    shape: torch.Size, mesh: DeviceMesh, placements: Sequence[Placement]
) -> torch.Size:
    """
    Compute the global size of a DTensor from the given local tensor shape,
    the mesh and placements. Different from `compute_global_tensor_info`,
    which assumes sharding is even, this util allgathers local shards' shapes
    from all ranks and thus can support uneven sharding.
    NOTE: Currently this function only supports 1D mesh.

    Args:
        shape (:class:`torch.Size`):
            Shape of the local tensor
        mesh (:class:`DeviceMesh`):
            Object which describes the mesh topology
            of devices for the DTensor.
        placements (Sequence[:class:`Placement`]]):
            The attribute of the DTensor that describes its layout
            on the mesh topology.

    Return:
        tensor_shape: Shape of the global DTensor.
    """
    if len(placements) != 1:
        raise NotImplementedError(
            "compute_global_tensor_shape only supports 1 placement for now."
        )

    if len(placements) != mesh.ndim:
        raise RuntimeError(
            "Expected one placement per mesh dim, "
            f"but found {len(placements)} placements and {mesh.ndim} mesh dims."
        )

    if isinstance(placements[0], Replicate):
        return shape
    # NOTE: isinstance(_, Shard) does not match _StridedShard; see _is_shard_like().
    elif isinstance(placements[0], Shard):

        @maybe_run_for_local_tensor
        def _create_local_shape_tensor(shape):
            return torch.tensor(list(shape), device=mesh.device_type)

        local_shape = _create_local_shape_tensor(shape)
        gathered_shaped_tensors = [
            torch.empty_like(local_shape, device=local_shape.device)
            for _ in range(mesh.size())
        ]
        funcol.all_gather_inplace(gathered_shaped_tensors, local_shape, mesh)

        @maybe_run_for_local_tensor
        def _validate_and_compute_global_shape(local_shape, gathered_shaped_tensors):
            sharded_dim_sum = 0
            shard_dim = placements[0].dim  # type: ignore[union-attr]
            other_dims = [d for d in range(len(shape)) if d != shard_dim]
            for shape_tensor in gathered_shaped_tensors:
                if not torch.equal(local_shape[other_dims], shape_tensor[other_dims]):
                    raise RuntimeError(
                        "Non-sharded dimensions should have identical size across ranks."
                    )
                shape_tensor_list = shape_tensor.tolist()
                sharded_dim_sum += shape_tensor_list[shard_dim]
            return sharded_dim_sum

        sharded_dim_sum = _validate_and_compute_global_shape(
            local_shape, gathered_shaped_tensors
        )
        global_shape = list(shape)
        global_shape[placements[0].dim] = sharded_dim_sum
        return torch.Size(global_shape)
    else:
        raise NotImplementedError(
            f"Placement type {type(placements[0])} not supported."
        )

