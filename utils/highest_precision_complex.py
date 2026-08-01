
def highest_precision_complex(device):
    if torch.device(device).type == "mps":
        return torch.complex64
    else:
        return torch.complex128

