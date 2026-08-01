
def _bucket_size_fusion(
    graph: fx.Graph, comm_blocks: list[CommBlock], bucket_size_mb: int
) -> Generator[list[CommBlock], None, None]:
    MB = 1024**2
    bucket_size = 1 * MB
    bucket_cap_size = bucket_size_mb * MB
    curr_size = 0
    curr_blocks = []

    count = 0
    fuse_count = 0
    for i, block in enumerate(comm_blocks):
        curr_blocks.append(block)
        itemsize = block.comm_node.meta["tensor_meta"].dtype.itemsize
        curr_size += cast(torch.Size, block.shape).numel() * itemsize
        count += 1
        if curr_size < bucket_size and i != len(comm_blocks) - 1:
            continue

        fuse_count += 1
        if torch.distributed.get_rank() == 0:
            logger.info(
                "DDP bucketing: block%d, count=%d, curr_size=%d, bucket_size=%d",
                fuse_count,
                count,
                curr_size,
                bucket_size,
            )

        # Set the debug counters
        counters["inductor"]["ddp_buckets"] = fuse_count
        yield curr_blocks

        bucket_size = bucket_cap_size
        curr_blocks = []
        curr_size = 0
        count = 0

