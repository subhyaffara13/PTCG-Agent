
def _pre_load_state_dict(
    tensor: torch.Tensor,
) -> tuple[torch.Tensor, list[Shard]]:
    shards = cast(ShardedTensor, tensor).local_shards()
    if len(shards) == 1 and type(shards[0].tensor) is ShardedTensor:
        inner_tensor = shards[0].tensor
        shards = inner_tensor.local_shards()  # pyre-ignore[16]
        tensor = inner_tensor

    return (tensor, shards if len(shards) > 0 else [])

