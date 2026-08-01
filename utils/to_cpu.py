
def to_cpu(tensors, devices=None):
    devices = devices or ["lazy"]

    flattened, spec = tree_flatten(tensors)
    sync_multi(flattened, devices)
    return tree_unflatten([t.to("cpu") for t in flattened], spec)

