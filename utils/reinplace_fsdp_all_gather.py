
def reinplace_fsdp_all_gather(graph: torch.fx.Graph) -> None:
    try:
        import torch.distributed.fsdp._fully_shard._fsdp_collectives

        assert torch.distributed.is_available()
        # Assert existence of these ops
        assert (
            torch.ops._c10d_functional.all_gather_into_tensor
            and torch.ops._c10d_functional.all_gather_into_tensor_out
        )
    except (ImportError, AttributeError, AssertionError):
        return

    from .pattern_matcher import (
        CallFunction,
        KeywordArg,
        Match,
        PatternMatcherPass,
        register_graph_pattern,
    )

    """
    all_gather_copy_in = torch.ops.fsdp.all_gather_copy_in.default(...);
    getitem = all_gather_copy_in[0];
    (getitem_1 = all_gather_copy_in[1];)  # optional

    all_gather_into_tensor = torch.ops._c10d_functional.all_gather_into_tensor.default(getitem, ...);

    ->

    all_gather_copy_in = torch.ops.fsdp.all_gather_copy_in.default(...);
    getitem = all_gather_copy_in[0];
    getitem_1 = all_gather_copy_in[1];

    all_gather_into_tensor = torch.ops._c10d_functional.all_gather_into_tensor_out.default(getitem, ..., out=getitem_1);
    """

    def remove_unused_getitem(g):
        # Remove `getitem_X = all_gather_copy_in[1]` which is never used.
        node_list = list(g.nodes)
        for n in node_list:
            if (
                n.target is operator.getitem
                and n.args[0].target is torch.ops.fsdp.all_gather_copy_in.default
                and n.args[1] == 1
            ):
                g.erase_node(n)

    graph_pass = PatternMatcherPass()

    @register_graph_pattern(
        CallFunction(
            torch.ops._c10d_functional.all_gather_into_tensor.default,
            CallFunction(
                operator.getitem,
                CallFunction(
                    torch.ops.fsdp.all_gather_copy_in.default,
                    KeywordArg("all_gather_inputs"),
                    KeywordArg("all_gather_output"),
                    KeywordArg("inp_split_sizes"),
                    KeywordArg("all_gather_input_numel"),
                    KeywordArg("rank"),
                ),
                KeywordArg("item_idx"),
            ),
            KeywordArg("group_size"),
            KeywordArg("group_name"),
        ),
        # pyrefly: ignore [bad-argument-type]
        pass_dict=graph_pass,
        extra_check=lambda match: match.kwargs["item_idx"] == 0,
    )
    def reinplace_all_gather(match: Match, *args, **kwargs):
        def repl(
            *args,
        ):
            copy_in_args = args[:-2]
            group_size = args[-2]
            group_name = args[-1]
            all_gather_copy_in = torch.ops.fsdp.all_gather_copy_in.default(
                *copy_in_args
            )
            getitem = all_gather_copy_in[0]
            getitem_1 = all_gather_copy_in[1]
            all_gather_into_tensor = (
                torch.ops._c10d_functional.all_gather_into_tensor_out.default(
                    getitem, group_size, group_name, out=getitem_1
                )
            )
            return all_gather_into_tensor

        match.replace_by_example(
            # pyrefly: ignore [bad-argument-type]
            repl,
            [
                kwargs["all_gather_inputs"],
                kwargs["all_gather_output"],
                kwargs["inp_split_sizes"],
                kwargs["all_gather_input_numel"],
                kwargs["rank"],
                kwargs["group_size"],
                kwargs["group_name"],
            ],
        )

    remove_unused_getitem(graph)
    graph_pass.apply(graph)  # type: ignore[arg-type]

