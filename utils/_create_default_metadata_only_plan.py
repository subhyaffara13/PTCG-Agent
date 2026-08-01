
def _create_default_metadata_only_plan(state_dict: STATE_DICT_TYPE) -> SavePlan:
    requests = []
    for fqn, obj in state_dict.items():
        if isinstance(obj, DTensor):
            requests.append(_create_write_items_for_dtensor(fqn, obj))
        elif isinstance(obj, ShardedTensor):
            requests.extend(
                _create_write_item_for_shard(fqn, obj, shard_md)
                for shard_md in obj.metadata().shards_metadata
            )
        elif isinstance(obj, torch.Tensor):
            requests.append(_create_write_item_for_tensor(fqn, obj))
        else:
            requests.append(_create_write_item_for_bytesio(fqn, obj))
    return SavePlan(requests)

