
def parse_module_info(module_info: ModuleInfo) -> Graph:
    """
    Parse module info and create a graph (tree) of modules. The graph will be
    used by MILP solver to find optimal SAC and/or FSDP configurations.
    """
    mod_stats = module_info["mod_stats"]
    fw_pre_order = module_info["mod_order"]["fw_pre_order"]
    # assertion and number of nodes
    if len(mod_stats) != len(fw_pre_order):
        raise AssertionError
    n_nodes = len(mod_stats)

    # create graph
    g = Graph(n_nodes)
    g.fw_post_order = module_info["mod_order"]["fw_post_order"]

    # sort the modules by pre-order and add them to the graph
    module_info["mod_stats"] = sorted(
        mod_stats, key=lambda x: fw_pre_order.index(x["fqn"])
    )
    for i, one_mod_stats in enumerate(mod_stats):
        node: Node = cast(Node, one_mod_stats)
        node["index"] = i
        node["pos_fw_post_order"] = g.fw_post_order.index(node["fqn"])
        g.add_node(node)

    # set up ancestor-descendant matrix
    for i in range(n_nodes):
        for j in range(i, n_nodes):
            if is_self_or_submodule(g.nodes[j]["fqn"], g.nodes[i]["fqn"]):
                g.ad_matrix[i][j] = 1
            else:
                break

    return g

