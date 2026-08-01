
def create_num_blocks_fake_generator(sparse_indices):
    """Create a fake num_blocks that is used for autotuning.

    The idea here is that we need to create a real tensor with real data
    that's representative for benchmarking.
    For example, returning all zeros for the `kv_num_blocks` input would mean
    that we are computing 0 blocks for each row, which would provide bogus
    autotuning results.

    In this case, we choose to use min(16, max_block) blocks, because I
    (Horace) think it'll probably result in pretty representative performance.
    If it's too short then prefetching won't help. If it's too long then
    autotuning will take longer for no good reason.
    """

    def create_num_blocks_fake(x) -> torch.Tensor:
        num_blocks_for_autotuning = V.graph.sizevars.optimization_hint(
            sparse_indices.shape[-1]
        )
        size = V.graph.sizevars.optimization_hints(x.get_size())
        return torch.full(
            size,
            num_blocks_for_autotuning,
            dtype=x.get_dtype(),
            device=x.get_device(),
        )

    return create_num_blocks_fake

