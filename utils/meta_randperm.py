
def meta_randperm(n, *, generator=None, out):
    return _maybe_resize_out(out, torch.Size([n]))

