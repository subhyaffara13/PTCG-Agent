
def _ext_pre_load_state_dict_transform(
    tensor: torch.Tensor,
    fsdp_extension: FSDPExtensions | None = None,
) -> tuple[torch.Tensor, list[Shard]]:
    if fsdp_extension is not None:
        return fsdp_extension.pre_load_state_dict_transform(tensor)

    if type(tensor) is not ShardedTensor:
        raise AssertionError(f"Expected ShardedTensor, got {type(tensor)}")
    shards = tensor.local_shards()
    return (tensor, shards)

