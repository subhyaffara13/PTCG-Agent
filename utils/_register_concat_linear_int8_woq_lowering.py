import copy

def _register_concat_linear_int8_woq_lowering(
    pattern, computation_woq, computation_reshape
):
    @register_freezing_graph_pattern(
        pattern,
        extra_check=_is_valid_concat_linear_int8_woq_optimization_pattern(),
        pass_number=4,
    )
    def woq_int8(match: Match, *args, **kwargs):
        x = kwargs["x"]
        w1 = kwargs["w1"]
        w2 = kwargs["w2"]
        w3 = kwargs["w3"]
        scales = kwargs["scales"]
        counters["inductor"]["woq_matcher_count"] += 1
        counters["inductor"]["woq_matcher_nodes"] += len(match.nodes)
        out_features = (
            w1.meta["val"].size()[0]
            + w2.meta["val"].size()[0]
            + w3.meta["val"].size()[0]
        )
        origin_x_size = tuple(x.meta["val"].size())
        x_shape = [-1, origin_x_size[-1]]
        out_shape = list(origin_x_size[:-1] + (out_features,))
        mm_node_of_x = None
        for candidate in iter(x.users.keys()):
            if (
                candidate.target is aten.mm.default
                and list(candidate._input_nodes)[1].target is aten.cat.default
            ):
                mm_node_of_x = candidate
                break
        assert mm_node_of_x is not None, "unable to find mm node"
        _, cat_wgt_node = mm_node_of_x._input_nodes
        scaling_node = next(iter(mm_node_of_x.users.keys()))
        user_of_scaling_node = next(iter(scaling_node.users.keys()))
        # Some other pass is making some changes that entails
        # adding a node before it's used, but it can only be found when
        # lint is run. stable_topological_sort() is being run before lint,
        # so that error was not being being discovered.
        # We call stable_topological_sort here as a workaround.
        stable_topological_sort(match.graph)
        with match.graph.inserting_before(user_of_scaling_node):
            new_cat_node = match.graph.call_function(
                aten.cat.default,
                args=([w1, w2, w3], 0),
            )
            x_reshape_node = match.graph.call_function(
                computation_reshape, args=(x, x_shape)
            )
            new_woq_node = match.graph.call_function(
                computation_woq,
                args=(x_reshape_node, new_cat_node, scales),
            )
            new_woq_node.meta = copy.copy(x.meta)
            output_reshape_node = match.graph.call_function(
                computation_reshape, args=(new_woq_node, out_shape)
            )
            scaling_node.replace_all_uses_with(output_reshape_node)
            match.graph.erase_node(scaling_node)
            match.graph.erase_node(mm_node_of_x)
            match.graph.erase_node(cat_wgt_node)
            match.graph.lint()

    return woq_int8

