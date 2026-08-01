
def gm_original_output_strides(gm: torch.fx.GraphModule) -> None:
    output_node = gm.graph.find_nodes(op="output")[0]
    output_node.meta["user_visible_output_idxs"] = [
        idx for idx, _ in enumerate(output_node.args)
    ]
    from torch._inductor.compile_fx import record_original_output_strides

    record_original_output_strides(gm)

