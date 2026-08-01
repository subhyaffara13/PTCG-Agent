
def _get_masked_fn(fn):
    if fn == "all":
        return _masked_all
    return getattr(torch.masked, fn)

