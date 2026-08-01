
def binop_reduce(tensors, op):
    res = op(torch.stack(tensors), dim=0)
    if isinstance(res, torch.Tensor):
        return res
    # min/max return a namedtuple
    return res.values

