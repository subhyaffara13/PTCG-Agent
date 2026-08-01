
def fp8_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    weight_scale_inv: torch.Tensor,
    block_size: list[int] | None = None,
    bias: torch.Tensor | None = None,
    activation_scale: torch.Tensor | None = None,
    output_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    """End-to-end FP8/FP4 linear used by `FP8Linear` and the eager `FP8Experts` loop.

    Dispatch order — both backends handle FP8 and FP4 weights with fp32 or UE8M0 scales:
      1. DeepGEMM (`deepgemm_fp8_fp4_linear`) — 3-6× faster on the shapes it supports.
         Preferred for FP4, UE8M0 SFs, and 128×128 block FP8.
      2. Triton finegrained-fp8 fallback — used when DeepGEMM is unavailable, when the
         caller passes ``activation_scale`` (DeepGEMM is dynamic-only), or for any
         shape DeepGEMM declined.

    Args:
        input: (..., K) bf16/fp16 activations.
        weight: (N, K) `float8_e4m3fn` or (N, K // 2) `int8` (FP4-packed).
        weight_scale_inv: per-block weight scales — `float32` (V3-style) or `float8_e8m0fnu`
            (V4-style; reinterpreted as int32 at the DeepGEMM kernel boundary).
        block_size: [block_n, block_k] for FP8 block-wise quant, or None/[N, K] for per-tensor.
            Ignored for FP4 weights (the kernel infers SF granularity from the dtype).
        bias: optional bias added to the matmul output.
        activation_scale: pass a per-tensor scalar to use static activation quant; leave `None`
            for dynamic (per-token) quant.
        output_dtype: desired output dtype.
    """
    # DeepGEMM is CUDA-only, dynamic-only, SM90+ only, FP4/FP8-block-128-only.
    # ``TRANSFORMERS_DISABLE_DEEPGEMM_LINEAR=1`` forces the Triton fallback for this single
    # dispatcher (the experts ``"deepgemm"`` impl is unaffected — use ``set_experts_implementation``
    # for that). Used by the FP8 MoE batched_mm / grouped_mm paths to avoid a still-unexplained
    # DeepGEMM-vs-Triton interaction that degrades end-to-end generation on B200 (per-row kernel
    # outputs still measure bit-perfect, but final tokens drift; not reproducible with the
    # DeepGEMM linear off). Also temporarily skipped under ``torch.compile`` — DeepGEMM's
    # per-token cast calls ``pack_ue8m0_to_int`` which has data-dependent bit-twiddling that
    # dynamo can't guard. TODO: remove the ``is_torchdynamo_compiling`` gate once the upstream
    # ``pack_ue8m0_to_int`` is rewritten to be FakeTensor-friendly; the Triton fallback is
    # dynamo-friendly today via its ``@triton_op`` registration.
    deepgemm_preferred = (
        activation_scale is None
        and weight.device.type == "cuda"
        and torch.cuda.get_device_properties().major >= 9
        and (weight.dtype == torch.int8 or (block_size is not None and block_size[0] == block_size[1] == 128))
        and os.environ.get("TRANSFORMERS_DISABLE_DEEPGEMM_LINEAR", "0") != "1"
        and not is_torchdynamo_compiling()
    )

    if deepgemm_preferred:
        try:
            return deepgemm_fp8_fp4_linear(
                input,
                weight,
                weight_scale_inv,
                block_size=block_size,
                output_dtype=output_dtype,
                activation_scale=activation_scale,
                bias=bias,
            )
        except ImportError as e:
            # Forward the original reason so the user knows whether DeepGEMM is unavailable
            # (env/build issue) or refused this specific input (e.g. multi-device on SM100).
            logger.warning_once(f"DeepGEMM unavailable for this call, falling back to Triton. Reason: {e}")

    return finegrained_fp8_linear(input, weight, weight_scale_inv, block_size, bias, activation_scale, output_dtype)

