
def fuse_ddp_with_coalesced_op(graph: fx.Graph, bucket_size_mb: int) -> None:
    _fuse_ddp_communication(
        graph,
        partial(_bucket_size_fusion, bucket_size_mb=bucket_size_mb),
        partial(_fuse_allreduce, use_concat=False),
    )

