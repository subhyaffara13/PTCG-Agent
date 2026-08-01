
def find_tensor_shard(tensor: torch.Tensor, index: MetadataIndex) -> torch.Tensor:
    if hasattr(tensor, "__get_tensor_shard__"):
        # DTensor implements _Checkpointable
        return tensor.__get_tensor_shard__(index)  # type: ignore[attr-defined]
    if isinstance(tensor, ShardedTensor):
        return _find_shard(tensor, index).tensor
    if index.offset is not None:
        # special case looking up a tensor by origin
        if index.offset == torch.Size([0] * len(tensor.size())):
            return tensor
        raise ValueError(
            f"FQN: '{index.fqn}' is not a ShardedTensor, can't find by offset: '{index.offset}'"
        )
    return tensor

