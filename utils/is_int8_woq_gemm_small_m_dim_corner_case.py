
def is_int8_woq_gemm_small_m_dim_corner_case(config, m, n, k):
    return (
        k % config.register_blocking.block_k == 0
        and n % config.register_blocking.block_n == 0
        and m < 16
    )

