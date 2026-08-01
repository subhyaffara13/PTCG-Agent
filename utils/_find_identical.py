
def _find_identical(
    tensors: list[set[str]], state_dict: dict[str, torch.Tensor]
) -> tuple[list[set[str]], list[set[str]]]:
    shared_tensors = []
    identical: list[set[str]] = []
    for shared in tensors:
        if len(shared) < 2:
            continue

        areas = collections.defaultdict(set)
        for name in shared:
            tensor = state_dict[name]
            area = (tensor.device, tensor.data_ptr(), _end_ptr(tensor))
            areas[area].add(name)
        if len(areas) == 1:
            identical.append(shared)
        else:
            shared_tensors.append(shared)
    return shared_tensors, identical

