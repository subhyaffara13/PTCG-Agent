
def simple_cond(x):
    return torch.cond(x.sum() > 2, lambda x: (x.cos(),), lambda x: (x.sin(),), [x])

