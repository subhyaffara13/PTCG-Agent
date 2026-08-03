from typing import Any

def find_state_dict_object(state_dict: STATE_DICT_TYPE, index: MetadataIndex) -> Any:
    if index.fqn not in state_dict:
        raise ValueError(f"Could not find FQN: '{index.fqn}'")
    obj = state_dict[index.fqn]

    if isinstance(obj, torch.Tensor):
        return find_tensor_shard(obj, index)
    elif index.offset is not None:
        raise ValueError(
            f"FQN: '{index.fqn}' is not a ShardedTensor, can't find by offset: '{index.offset}'"
        )
    return obj

