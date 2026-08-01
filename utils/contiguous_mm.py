
def contiguous_mm(a, b):
    return torch.mm(a, b.contiguous())

