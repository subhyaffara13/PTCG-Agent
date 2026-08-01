
def _find_shared_tensors(state_dict: Dict[str, torch.Tensor]) -> List[Set[str]]:
    tensors = defaultdict(set)
    for k, v in state_dict.items():
        if (
            v.device != torch.device("meta")
            and storage_ptr(v) != 0
            and storage_size(v) != 0
        ):
            # Need to add device as key because of multiple GPU.
            tensors[(v.device, storage_ptr(v), storage_size(v))].add(k)
    tensors = list(sorted(tensors.values()))
    tensors = _filter_shared_not_shared(tensors, state_dict)
    return tensors


def _find_shared_tensors(state_dict: dict[str, "torch.Tensor"]) -> list[set[str]]:
    """
    Taken from https://github.com/huggingface/safetensors/blob/079781fd0dc455ba0fe851e2b4507c33d0c0d407/bindings/python/py_src/safetensors/torch.py#L69.
    """
    import torch

    tensors_dict = defaultdict(set)
    for k, v in state_dict.items():
        if v.device != torch.device("meta") and storage_ptr(v) != 0 and get_torch_storage_size(v) != 0:
            # Need to add device as key because of multiple GPU.
            tensors_dict[(v.device, storage_ptr(v), get_torch_storage_size(v))].add(k)
    tensors = list(sorted(tensors_dict.values()))
    tensors = _filter_shared_not_shared(tensors, state_dict)
    return tensors

