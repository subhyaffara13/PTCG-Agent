
def fuse_by_partitions(
    gm: GraphModule,
    partitions: list[dict[Node, int | None]],
    prefix: str = "fused_",
    always_return_tuple: bool = False,
) -> GraphModule:
    for partition_id, partition in enumerate(partitions):
        sorted_nodes = topo_sort(list(partition))

        submodule_name = prefix + str(partition_id)
        sub_gm, orig_inputs, orig_outputs = fuse_as_graphmodule(
            gm,
            sorted_nodes,
            submodule_name,
            partition,
            always_return_tuple=always_return_tuple,
        )

        insert_subgm(gm, sub_gm, orig_inputs, orig_outputs, sorted_nodes[-1])

        erase_nodes(gm, sorted_nodes)

    torch.fx.passes.tools_common.stable_topological_sort(gm)
    gm.graph.lint()

    return gm

