
def is_compute_node(n: fx.Node) -> bool:
    """
    Should we consider this node computationally expensive ?
    Currently uses flop registration, but we could expand more generally.
    """
    return (
        getattr(n.target, "overloadpacket", None)
        in torch.utils.flop_counter.flop_registry
    )

