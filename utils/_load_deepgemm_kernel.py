
def _load_deepgemm_kernel(requires_sm100: bool = False) -> DeepGEMM:
    """Load DeepGEMM once; raise `ImportError` if env or any required symbol is missing.

    `requires_sm100` raises a Blackwell-specific error for callers (FP4 / Mega MoE)
    that won't work on Hopper, instead of the generic SM90+ message.
    """
    if not is_torchdynamo_compiling():
        if not is_kernels_available():
            raise ImportError(
                "DeepGEMM kernel requires the `kernels` package. Install it with `pip install -U kernels`."
            )
        if not torch.cuda.is_available():
            raise ImportError("DeepGEMM kernel requires CUDA, but CUDA is not available.")

        major, minor = torch.cuda.get_device_capability()
        # DeepGEMM ships kernels only for SM90 (Hopper) and SM100 (Blackwell); anything
        # else — Ada (SM89), Ampere (SM80), or future archs (SM110+) — has no build.
        allowed = (10,) if requires_sm100 else (9, 10)
        if major not in allowed:
            arch = "Blackwell (SM100)" if requires_sm100 else "Hopper (SM90) or Blackwell (SM100)"
            raise ImportError(f"DeepGEMM requires {arch}; current device is SM{major}{minor}.")

        # Per the DeepGEMM README: SM90 needs CUDA 12.3+, SM100 needs CUDA 12.9+.
        cuda_major, cuda_minor = get_cuda_runtime_version()
        min_cuda = (12, 9) if major == 10 else (12, 3)
        if (cuda_major, cuda_minor) < min_cuda:
            raise ImportError(
                f"DeepGEMM on SM{major}{minor} requires CUDA runtime ≥ {min_cuda[0]}.{min_cuda[1]}, "
                f"found {cuda_major}.{cuda_minor}."
            )

    kernel = lazy_load_kernel("deep-gemm")
    if kernel is None:
        raise ImportError(
            "Failed to load `kernels-community/deep-gemm` — check that a build matches the current torch/CUDA."
        )

    fp8_fp4_matmul = getattr(kernel, "fp8_fp4_gemm_nt", None)
    grouped_fp8_fp4_matmul_nt = getattr(kernel, "m_grouped_fp8_fp4_gemm_nt_contiguous", None)
    grouped_fp8_fp4_matmul_nn = getattr(kernel, "m_grouped_fp8_fp4_gemm_nn_contiguous", None)
    grouped_bf16_matmul_nt = getattr(kernel, "m_grouped_bf16_gemm_nt_contiguous", None)
    grouped_bf16_matmul_nn = getattr(kernel, "m_grouped_bf16_gemm_nn_contiguous", None)
    per_token_cast_to_fp8 = resolve_internal_import(kernel, chained_path="utils.per_token_cast_to_fp8")
    transform_sf_into_required_layout = getattr(kernel, "transform_sf_into_required_layout", None)
    transform_weights_for_mega_moe = getattr(kernel, "transform_weights_for_mega_moe", None)
    get_symm_buffer_for_mega_moe = getattr(kernel, "get_symm_buffer_for_mega_moe", None)
    get_mk_alignment = getattr(kernel, "get_mk_alignment_for_contiguous_layout", None)
    fp8_fp4_mega_moe = getattr(kernel, "fp8_fp4_mega_moe", None)

    missing = [
        name
        for name, attr in [
            ("fp8_fp4_gemm_nt", fp8_fp4_matmul),
            ("m_grouped_fp8_fp4_gemm_nt_contiguous", grouped_fp8_fp4_matmul_nt),
            ("m_grouped_fp8_fp4_gemm_nn_contiguous", grouped_fp8_fp4_matmul_nn),
            ("m_grouped_bf16_gemm_nt_contiguous", grouped_bf16_matmul_nt),
            ("m_grouped_bf16_gemm_nn_contiguous", grouped_bf16_matmul_nn),
            ("utils.per_token_cast_to_fp8", per_token_cast_to_fp8),
            ("transform_sf_into_required_layout", transform_sf_into_required_layout),
            ("transform_weights_for_mega_moe", transform_weights_for_mega_moe),
            ("get_symm_buffer_for_mega_moe", get_symm_buffer_for_mega_moe),
            ("get_mk_alignment_for_contiguous_layout", get_mk_alignment),
            ("fp8_fp4_mega_moe", fp8_fp4_mega_moe),
        ]
        if attr is None
    ]
    if missing:
        raise ImportError(
            f"DeepGEMM kernel is missing required symbols: {', '.join(missing)}. Update with `pip install -U kernels`."
        )
    return DeepGEMM(
        fp8_fp4_matmul=fp8_fp4_matmul,
        grouped_fp8_fp4_matmul_nt=grouped_fp8_fp4_matmul_nt,
        grouped_fp8_fp4_matmul_nn=grouped_fp8_fp4_matmul_nn,
        grouped_bf16_matmul_nt=grouped_bf16_matmul_nt,
        grouped_bf16_matmul_nn=grouped_bf16_matmul_nn,
        per_token_cast_to_fp8=per_token_cast_to_fp8,
        transform_sf_into_required_layout=transform_sf_into_required_layout,
        transform_weights_for_mega_moe=transform_weights_for_mega_moe,
        get_symm_buffer_for_mega_moe=get_symm_buffer_for_mega_moe,
        fp8_fp4_mega_moe=fp8_fp4_mega_moe,
        m_alignment=int(get_mk_alignment()),
    )

