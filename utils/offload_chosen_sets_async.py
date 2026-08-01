
def offload_chosen_sets_async(
    fwd_module: fx.GraphModule,
    bwd_module: fx.GraphModule,
) -> None:
    """
    Add async offload and reload nodes using ao ops.

    Uses ao.offload/ao.reload + ao.wait_tensor which encapsulate stream management,
    instead of device_put + explicit stream operations. Can be applied to
    partitioned forward/backward graphs or to a joint graph produced by make_fx.
    """

    offload_activation_fw_async(fwd_module.graph)

    # Replace backward graph placeholders with their offloaded (CPU) counterparts.
    # For each offloaded forward output, find the matching backward input and swap
    # it with a new placeholder carrying the CPU tensor's metadata, then mark it
    # for reloading.
    bwd_inputs: dict[str, fx.Node] = {
        node.name: node for node in bwd_module.graph.find_nodes(op="placeholder")
    }
    for fwd_node in fwd_module.graph.find_nodes(op="output")[0].args[0]:
        if CPU_OFFLOAD_PREFIX not in fwd_node.name:
            continue

        bwd_node: fx.Node = bwd_inputs[fwd_node.name.replace(CPU_OFFLOAD_PREFIX, "")]
        with bwd_module.graph.inserting_after(bwd_node):
            bwd_offload_node: fx.Node = bwd_module.graph.placeholder(name=fwd_node.name)

        bwd_offload_node.meta.update(fwd_node.meta)
        bwd_offload_node.meta["saved_for_offloading"] = True
        bwd_offload_node.meta["original_device"] = bwd_node.meta["val"].device
        bwd_node.replace_all_uses_with(bwd_offload_node)
        bwd_module.graph.erase_node(bwd_node)

    reload_activation_bw_async(bwd_module.graph)

