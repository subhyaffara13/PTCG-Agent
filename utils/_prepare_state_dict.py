
def _prepare_state_dict(
    state_dict: object,
    device: torch.device,
) -> tuple[_StateDictMeta, list[torch.Tensor]]:
    leaves: list[tuple[KeyPath, object]]
    leaves, treespec = tree_flatten_with_path(state_dict)

    paths: list[KeyPath] = []
    non_tensor_leaves: list[
        object | _TensorMeta | _DTensorMeta | _ShardedTensorMeta
    ] = []
    tensors: list[torch.Tensor] = []
    for key_path, v in leaves:
        paths.append(key_path)

        if isinstance(v, DTensor):
            tensor, tensor_meta = _prepare_tensor(v._local_tensor)

            tensors.append(tensor)

            non_tensor_leaves.append(
                _DTensorMeta(
                    local=tensor_meta,
                    spec=v._spec,
                )
            )
        elif isinstance(v, ShardedTensor):
            # Handle ShardedTensor by extracting all local shards
            local_shards = v.local_shards()

            # Prepare metadata for all local shards
            local_shards_meta = []
            local_shards_shard_metadata = []
            for shard in local_shards:
                tensor, tensor_meta = _prepare_tensor(shard.tensor)
                tensors.append(tensor)
                local_shards_meta.append(tensor_meta)
                local_shards_shard_metadata.append(shard.metadata)

            non_tensor_leaves.append(
                _ShardedTensorMeta(
                    local_shards_meta=local_shards_meta,
                    local_shards_shard_metadata=local_shards_shard_metadata,
                    sharded_tensor_metadata=v.metadata(),  # Complete metadata
                )
            )
        elif isinstance(v, torch.Tensor):
            tensor, tensor_meta = _prepare_tensor(v)
            tensors.append(tensor)
            non_tensor_leaves.append(tensor_meta)
        else:
            non_tensor_leaves.append(v)

    return (
        _StateDictMeta(
            treespec=treespec,
            paths=paths,
            non_tensor_leaves=non_tensor_leaves,
        ),
        tensors,
    )

