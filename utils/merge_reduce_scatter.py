
def merge_reduce_scatter(
    gm: torch.fx.GraphModule,
    rs_buckets: list[list[torch.fx.Node]],
    mode: BucketMode | None = None,
) -> None:
    """
    Merges specified buckets of reduce_scatter to joint reduce_scatter.
    """
    mode = mode or _default_bucket_mode()
    with dynamo_timed("fx.bucketing.merge_reduce_scatter", log_pt2_compile_event=True):
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "fx_bucketing_passes_reduce_scatter_buckets",
                "encoding": "string",
            },
            payload_fn=lambda: str(rs_buckets),
        )

        g = gm.graph

        for rs_nodes in rs_buckets:
            merge_reduce_scatter_bucket(g, rs_nodes, mode)

