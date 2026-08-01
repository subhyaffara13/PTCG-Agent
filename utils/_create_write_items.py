
def _create_write_items(fqn: str, object: Any) -> list[WriteItem]:
    if hasattr(object, "__create_write_items__"):
        # DTensor implements _Checkpointable
        return object.__create_write_items__(fqn, object)
    elif isinstance(object, ShardedTensor):
        return [
            _create_write_item_for_shard(fqn, object, shard.metadata)
            for shard in object.local_shards()
        ]
    elif isinstance(object, torch.Tensor):
        return [_create_write_item_for_tensor(fqn, object)]
    else:
        return [_create_write_item_for_bytesio(fqn, object)]

