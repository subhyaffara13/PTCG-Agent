import copy

def build_global_metadata(
    gathered_metadatas: Sequence[ShardedTensorMetadata | None],
    recalc_metadata: bool = False,
):
    global_sharded_tensor_metadata = None
    global_metadata_rank = 0

    # pyrefly: ignore [bad-assignment]
    for rank, rank_metadata in enumerate(gathered_metadatas):
        if rank_metadata is None:
            continue

        if global_sharded_tensor_metadata is None:
            global_sharded_tensor_metadata = copy.deepcopy(rank_metadata)
            global_metadata_rank = rank
        else:
            _raise_if_mismatch(
                global_sharded_tensor_metadata.size,
                rank_metadata.size,
                "global_size",
                [global_metadata_rank, rank],
                is_local=False,
            )

            # don't need to check layout and memory format as we already checked in local shards validation stage
            _raise_if_mismatch(
                global_sharded_tensor_metadata.tensor_properties.dtype,
                rank_metadata.tensor_properties.dtype,
                "dtype",
                [global_metadata_rank, rank],
                is_local=False,
            )

            _raise_if_mismatch(
                global_sharded_tensor_metadata.tensor_properties.requires_grad,
                rank_metadata.tensor_properties.requires_grad,
                "requires_grad",
                [global_metadata_rank, rank],
                is_local=False,
            )

            _raise_if_mismatch(
                global_sharded_tensor_metadata.tensor_properties.pin_memory,
                rank_metadata.tensor_properties.pin_memory,
                "pin_memory",
                [global_metadata_rank, rank],
                is_local=False,
            )
            # pass all validations, extend shards metadata
            global_sharded_tensor_metadata.shards_metadata.extend(
                rank_metadata.shards_metadata
            )

    if global_sharded_tensor_metadata is not None:
        if recalc_metadata:
            recalc_global_sharded_tensor_metadata(
                global_sharded_tensor_metadata,
                0,  # sharded on 0th dim
            )

        # check if shards_metadata have overlap shards
        validate_non_overlapping_shards_metadata(
            global_sharded_tensor_metadata.shards_metadata
        )

        # check if the shards_metadata is compatible with global size of the sharded tensor.
        check_tensor(
            global_sharded_tensor_metadata.shards_metadata,
            global_sharded_tensor_metadata.size,
        )
    else:
        raise ValueError("ShardedTensor have no local shards on all ranks!")

    return global_sharded_tensor_metadata

