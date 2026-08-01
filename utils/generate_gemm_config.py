
def generate_gemm_config(
    vec_isa_cls,
    register_blockings,
    input_dtype=torch.float,
    input2_dtype=None,
    output_dtype=None,
    compute_dtype=None,
    extra_check=None,
):
    if output_dtype is None:
        output_dtype = input_dtype
    if compute_dtype is None:
        compute_dtype = output_dtype
    if input2_dtype is None:
        input2_dtype = input_dtype
    return [
        CppMicroGemmConfig(
            input_dtype,
            input2_dtype,
            output_dtype,
            compute_dtype,
            vec_isa_cls,
            GemmBlocking(*blocking),
            extra_check,
        )
        for blocking in register_blockings
    ]

