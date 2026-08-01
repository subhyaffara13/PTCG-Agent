
def get_independent_tensor(tensor):
    return tensor.clone().requires_grad_(tensor.requires_grad)

