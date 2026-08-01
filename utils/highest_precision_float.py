
def highest_precision_float(device):
    if torch.device(device).type == "mps":
        return torch.float32
    else:
        return torch.float64

