
def countable_fx(node: torch.fx.Node) -> bool:
    """
    Whether or not we can count the flops of an FX node.
    """
    assert isinstance(node, torch.fx.Node)
    if not hasattr(node, "target"):
        return False
    target = node.target
    if not hasattr(target, "overloadpacket"):
        return target in flop_registry
    packet = target.overloadpacket
    return packet in flop_registry

