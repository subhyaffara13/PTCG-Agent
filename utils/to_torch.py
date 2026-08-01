
def to_torch(array):
    torch, device = _get_torch_and_device()

    if has_array_interface(array):
        return torch.from_numpy(array).to(device)

    return array

