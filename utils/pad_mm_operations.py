
def pad_mm_operations() -> list[AHOperation]:
    mult_dims_ops = get_mult_dims_ops()
    k_div_m_times_n_op = AHOperation(
        "k/(m*n)", lambda data: data["k"] / (data["m"] * data["n"])
    )

    def bfloat_perf_hit(data: Any) -> bool:
        m = data["m"]
        k = data["k"]
        n = data["n"]
        is_bfloat = str(data["mat1_dtype"]) == "torch.bfloat16"
        return k > (m * 1024) and k > (n * 1024) and is_bfloat

    bfloat_perf_hit_op = AHOperation(
        "bfloat_perf_hit", bfloat_perf_hit, is_categorical=True
    )

    arith_intensity_op = AHOperation("arith_intensity", get_arith_intensity)
    dims_need_padding_ops = get_dims_need_padding_ops()
    dims_multiple_ops = get_dims_multiple_ops()
    is_contig_ops = get_is_contig_ops()

    ah_operations = mult_dims_ops + [
        k_div_m_times_n_op,
        bfloat_perf_hit_op,
        arith_intensity_op,
    ]
    ah_operations.extend(dims_need_padding_ops)
    ah_operations.extend(dims_multiple_ops)
    ah_operations.extend(is_contig_ops)
    return ah_operations

