
def dump_state(fx_g: fx.GraphModule, inps: Sequence[torch.Tensor]) -> None:
    print(
        f"""
# Working Repro with {len(fx_g.graph.nodes)} nodes
inps = {[(i.shape, i.dtype, i.device.type) for i in inps]}
inps = [torch.zeros(())] + [torch.ones(shape, dtype=dtype, device=device) for (shape, dtype, device) in inps]
{fx_g.code}
"""
    )

