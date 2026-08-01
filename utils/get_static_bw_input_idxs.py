
def get_static_bw_input_idxs(fx_g: torch.fx.GraphModule) -> list[int]:
    """
    Returns indices of backward graph inputs that are always at fixed
    addresses: primals (parameters/buffers/user inputs saved for backward).
    Excludes saved activations which may not be at fixed addresses when
    the forward is partitioned for CUDA graphs.
    """
    static_idxs = []
    for idx, n in enumerate(fx_g.graph.nodes):
        if n.op != "placeholder":
            break
        if n.name.startswith("primals_"):
            static_idxs.append(idx)
    return static_idxs

