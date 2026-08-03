from typing import Any

def merge_reduce_scatter_bucket(
    g: torch.fx.Graph,
    rs_nodes: list[torch.fx.Node],
    mode: BucketMode | None = None,
    insert_before: torch.fx.Node | None = None,
    wait_insertion_point: torch.fx.Node | None = None,
) -> tuple[list[torch.fx.Node], dict[torch.fx.Node, torch.fx.Node]]:
    mode = mode or _default_bucket_mode()
    # Validate bucket consistency
    rs0 = rs_nodes[0]
    rs0_val = rs0.meta["val"]
    _, reduce_op, group_size, group_name = rs0.args
    reduce_dtype = rs0_val.dtype
    device = rs0_val.device

    for n in rs_nodes:
        rs_val = n.meta["val"]
        assert (
            n.args[1] == reduce_op
            and n.args[2] == group_size
            and n.args[3] == group_name
            and rs_val.device == device
            and rs_val.dtype == reduce_dtype
        )

    # Choose merge function based on mode
    rs_merge_fn = reduce_scatter_merge_fn_to_trace
    if mode == "coalesced":
        rs_merge_fn = reduce_scatter_merge_fn_coalesced
    elif mode and "custom_ops" in mode:
        rs_merge_fn = reduce_scatter_merge_fn_to_trace_custom_ops

    # Process bucket with lazy input collection
    def create_trace_args(bucket_ins: list[torch.fx.Node]) -> tuple[Any, ...]:
        return (
            pytree.tree_map(lambda node: node.meta["val"], bucket_ins),
            group_size,
            group_name,
            reduce_op,
            reduce_dtype,
            device,
        )

    return process_collective_bucket(
        g,
        rs_nodes,
        rs_merge_fn,
        create_trace_args,
        insert_before=insert_before,
        wait_insertion_point=wait_insertion_point,
    )

