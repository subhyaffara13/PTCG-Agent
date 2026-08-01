
def _swap_module_helper(
    gm: torch.fx.GraphModule,
    modules_to_swap: dict[str, torch.nn.Module],
    module_call_graph: dict[str, ModuleCallSignature],
) -> torch.fx.GraphModule:
    log.debug("Starting graph:")
    log.debug(gm.graph)

    legalize_graph(gm)

    partitions: dict[str, NodeList] = defaultdict(list)

    node_name_map: dict[str, torch.fx.Node] = {
        node.name: node for node in gm.graph.nodes
    }

    # TODO: Handle the duplicate module case
    for node in gm.graph.nodes:
        if nn_module_stack := node.meta.get("nn_module_stack"):
            for path, _ in nn_module_stack.values():
                if path in modules_to_swap:
                    partitions[path].append(node)
                    break

    for name, nodes in partitions.items():
        """
        Given a graph like the following, and we want to swap out the submodule "foo":
        graph():
            %x : [num_users=1] = placeholder[target=x]
            %y : [num_users=2] = placeholder[target=y]
            %add : [num_users=1] = call_function[target=torch.ops.aten.add.Tensor](args = (%y, %x), kwargs = {}), nn_module_stack = {"foo": ("foo", torch.nn.Module)}
            %sub : [num_users=1] = call_function[target=torch.ops.aten.sub.Tensor](args = (%y, %add), kwargs = {}), nn_module_stack = {"bar": ("bar", torch.nn.Module)}
            return (sub,)

        We will first partition out foo's subgraph:
        graph():
            %x : [num_users=1] = placeholder[target=x]
            %y : [num_users=2] = placeholder[target=y]
            %add : [num_users=1] = call_function[target=torch.ops.aten.add.Tensor](args = (%y, %x), kwargs = {})
            return add

        And then insert an unflatten + call_module + flatten to replace the subgraph:
        graph():
            %x : [num_users=1] = placeholder[target=x]
            %y : [num_users=1] = placeholder[target=y]

            %_spec_0 : [num_users=1] = get_attr[target=_spec_0]
            %tree_unflatten : [num_users=2] = call_function[target=torch.utils._pytree.tree_unflatten](args = ([%x, %y], %_spec_0), kwargs = {})
            %getitem : [num_users=2] = call_function[target=operator.getitem](args = (%tree_unflatten, 0), kwargs = {})
            %getitem_1 : [num_users=1] = call_function[target=operator.getitem](args = (%getitem, 0), kwargs = {})
            %getitem_2 : [num_users=1] = call_function[target=operator.getitem](args = (%getitem, 1), kwargs = {})
            %getitem_3 : [num_users=0] = call_function[target=operator.getitem](args = (%tree_unflatten, 1), kwargs = {})
            %foo : [num_users=0] = call_module[target=foo](args = (%getitem_1, %getitem_2), kwargs = {})
            %_spec_1 : [num_users=1] = get_attr[target=_spec_1]
            %tree_flatten_spec : [num_users=1] = call_function[target=torch.fx._pytree.tree_flatten_spec](args = (None, %_spec_1), kwargs = {})
            %getitem_4 : [num_users=1] = call_function[target=operator.getitem](args = (%tree_flatten_spec, 0), kwargs = {})

            %sub : [num_users=1] = call_function[target=torch.ops.aten.sub.Tensor](args = (%y, %getitem_4), kwargs = {})
            return (%sub,)

        The `tree_unflatten` call will construct tensor inputs into the input
        format needed by the swapped eager module.
        The `call_module` node should now reference the swapped torch.nn.Module.
        The `tree_flatten_spec` call will deconstruct the eager outputs of the
        swapped module into tensors.
        """  # noqa: B950

        submod_name = name.replace(".", "_")
        sub_gm, orig_inputs, orig_outputs = fuse_as_graphmodule(
            gm, nodes, f"fused_{submod_name}"
        )

        log.debug("Fused subgraph nodes:")
        log.debug(sub_gm.graph)

        signature: ModuleCallSignature = module_call_graph[name]

        args_nodes, kwargs_nodes = _construct_inputs(gm, signature, node_name_map)
        module_node = _insert_call_module(
            gm, args_nodes, kwargs_nodes, modules_to_swap[name], name
        )
        _deconstruct_outputs(gm, signature, module_node, node_name_map, orig_outputs)

        erase_nodes(gm, nodes)

        log.debug("Swapped graph:")
        log.debug(gm.graph)

    legalize_graph(gm)

    log.debug("Before removing extraneous pytrees:")
    log.debug(gm.graph)

    _remove_extraneous_pytrees(gm)
    log.debug("After removing extraneous pytrees:")
    log.debug(gm.graph)

    gm.recompile()

    return gm

