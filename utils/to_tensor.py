
def to_tensor(X, device):
    if not isinstance(X, torch.Tensor):
        X = torch.tensor(X)
    else:
        X = X.detach().clone()
    return X.to(device=torch.device(device), dtype=torch.float32)

