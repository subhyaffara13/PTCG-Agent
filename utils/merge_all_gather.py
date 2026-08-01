
def merge_all_gather(
    gm: torch.fx.GraphModule,
    ag_buckets: list[list[torch.fx.Node]],
    mode: BucketMode | None = None,
) -> None:
    """
    Merges specified buckets of all_gather to joint all_gather.
    """
    mode = mode or _default_bucket_mode()
    with dynamo_timed("fx.bucketing.merge_all_gather", log_pt2_compile_event=True):
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "fx_bucketing_passes_all_gather_buckets",
                "encoding": "string",
            },
            payload_fn=lambda: str(ag_buckets),
        )

        g = gm.graph

        for ag_nodes in ag_buckets:
            merge_all_gather_bucket(g, ag_nodes, mode)

