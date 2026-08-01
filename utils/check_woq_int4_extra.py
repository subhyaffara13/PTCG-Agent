
def check_woq_int4_extra(config, m, n, k, alpha, num_threads, **kwargs):
    if alpha != 1:
        return False
    q_group_size = kwargs.get("q_group_size")
    assert q_group_size is not None
    if (
        q_group_size not in [32, 64, 128]
        or k % q_group_size != 0
        or config.register_blocking.block_k > q_group_size
    ):
        return False
    return k % config.register_blocking.block_k == 0 and n % 64 == 0

