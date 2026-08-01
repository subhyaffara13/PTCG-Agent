
def simple_local_map_hop(inp1, inp2):
    def body_gm(inp1, inp2):
        return inp1.cos() + inp2.sin()

    gm = torch.fx.symbolic_trace(body_gm)

    if not torch.distributed.is_available():
        raise AssertionError("Expected torch.distributed to be available")
    from torch.distributed.tensor.placement_types import Replicate

    gm.meta["local_map_kwargs"] = {
        "in_placements": (Replicate(), Replicate(), Replicate()),
        "out_placements": ((Replicate(), Replicate(), Replicate()),),
    }

    # TODO: Dynamo would rewrite this op differently
    return torch._higher_order_ops.local_map_hop(gm, inp1, inp2)

