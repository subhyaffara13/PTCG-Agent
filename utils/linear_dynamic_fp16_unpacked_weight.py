
def linear_dynamic_fp16_unpacked_weight(
    input: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor | None = None,
) -> torch.Tensor:
    packed_weight = torch.ops._quantized.wrapped_fbgemm_pack_gemm_matrix_fp16(weight)
    return torch.ops._quantized.wrapped_fbgemm_linear_fp16_weight(
        input, packed_weight, bias, weight.size()[0]
    )

