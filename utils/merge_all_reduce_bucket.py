
def merge_all_reduce_bucket(
    g: torch.fx.Graph,
    ar_nodes: list[torch.fx.Node],
    mode: str | None = None,
    insert_before: torch.fx.Node | None = None,
    wait_insertion_point: torch.fx.Node | None = None,
) -> tuple[list[torch.fx.Node], dict[torch.fx.Node, torch.fx.Node]]:
    ar0 = ar_nodes[0]
    ar0_val = ar0.meta["val"]
    _, reduce_op, group_name = ar0.args
    reduce_dtype = ar0_val.dtype
    device = ar0_val.device

    for n in ar_nodes:
        ar_val = n.meta["val"]
        assert (
            n.args[1] == reduce_op
            and n.args[2] == group_name
            and ar_val.device == device
            and ar_val.dtype == reduce_dtype
        )

    ar_merge_fn = all_reduce_merge_fn_to_trace

    def create_trace_args(bucket_ins: list[torch.fx.Node]) -> tuple[Any, ...]:
        return (
            pytree.tree_map(lambda node: node.meta["val"], bucket_ins),
            group_name,
            reduce_op,
            reduce_dtype,
            device,
        )

    return process_collective_bucket(
        g,
        ar_nodes,
        ar_merge_fn,
        create_trace_args,
        insert_before=insert_before,
        wait_insertion_point=wait_insertion_point,
    )

