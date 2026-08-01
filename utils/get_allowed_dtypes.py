
def get_allowed_dtypes() -> list[torch.dtype]:
    allowed_dtypes = torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("allowed_dtypes", "torch.bfloat16")
    allowed_dtypes = [
        getattr(torch, dtype.split(".")[-1]) for dtype in allowed_dtypes.split(";")
    ]
    return allowed_dtypes

