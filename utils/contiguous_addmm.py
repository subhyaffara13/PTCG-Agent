
def contiguous_addmm(inp, a, b):
    return torch.addmm(inp, a, b.contiguous())

