
def get_fake(x):
    if isinstance(x, torch.fx.Node):
        if "val" not in x.meta:
            return x
        return x.meta["val"]
    return x

