
def _keep_visiting_tensors(value: STATE_DICT_ITEM) -> TypeIs[torch.Tensor]:
    return isinstance(value, torch.Tensor)

