
def get_mult_dims_ops() -> list[AHOperation]:
    m_times_k_op = AHOperation("m*k", lambda data: data["m"] * data["k"])
    m_times_n_op = AHOperation("m*n", lambda data: data["m"] * data["n"])
    k_times_n_op = AHOperation("k*n", lambda data: data["k"] * data["n"])
    return [m_times_k_op, m_times_n_op, k_times_n_op]

