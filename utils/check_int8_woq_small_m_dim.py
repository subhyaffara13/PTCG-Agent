
def check_int8_woq_small_m_dim(config, m, n, k, alpha, num_threads, **kwargs):
    return is_int8_woq_gemm_small_m_dim_corner_case(config, m, n, k) and not kwargs.get(
        "dynamic_M", False
    )

