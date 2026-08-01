
def deepgemm_fp8_fp4_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    weight_scale_inv: torch.Tensor,
    bias: torch.Tensor | None = None,
    block_size: tuple[int, int] | None = None,
    output_dtype: torch.dtype = torch.bfloat16,
    activation_scale: torch.Tensor | None = None,
) -> torch.Tensor:
    """End-to-end DeepGEMM linear: per-token activation quant + FP8/FP4 matmul.

    Static (per-tensor) activation quantization is rejected — DeepGEMM needs
    per-row SFs. Callers should route static activations through the Triton fallback.
    """
    _assert_single_device(input.device, context="linear")

    if activation_scale is not None:
        raise NotImplementedError("DeepGEMM linear does not support static activation quantization.")
    if input.dtype not in (torch.bfloat16, torch.float16):
        raise ValueError(f"DeepGEMM linear requires FP16 or BF16 activations, got {input.dtype}")

    deepgemm = load_deepgemm_kernel(requires_sm100=weight.dtype == torch.int8)
    cast_kwargs = _select_fp8_cast_kwargs(weight, weight_scale_inv, block_size, _is_sm100(input.device))

    input_2d = input.view(-1, input.shape[-1])
    qinput_2d, scale_2d = deepgemm.per_token_cast_to_fp8(input_2d, **cast_kwargs)
    output = torch.empty(qinput_2d.shape[0], weight.shape[0], device=input.device, dtype=output_dtype)

    # Pass `(1, 1, gran_k)` for int-SF paths so the kernel uses the right K granularity
    # (the default `(1, 1, 128)` mismatches FP4's gran_k=32). Float-SF leaves it None.
    sf_recipe = (1, 1, cast_kwargs["gran_k"]) if cast_kwargs.get("use_packed_ue8m0") else None
    deepgemm.fp8_fp4_matmul(
        (qinput_2d, _coerce_sf_for_kernel(scale_2d, expected_mn=qinput_2d.size(0))),
        (weight, _coerce_sf_for_kernel(weight_scale_inv, expected_mn=weight.size(0))),
        output,
        recipe=sf_recipe,
    )
    output = output.view(input.shape[:-1] + (weight.shape[0],))
    if bias is not None:
        output.add_(bias)
    return output

