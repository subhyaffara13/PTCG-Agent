
def _is_releasable(n: fx.Node) -> bool:
    # Storages of primals cannot be released during fwd or bwd pass.
    return not n.name.startswith("primals")

