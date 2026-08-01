
def get_sample_alignment_heads(
    config: WhisperConfig,
    device: torch.device,
    num_alignment_heads: int = 6,
    use_int32: bool = True,
):
    torch_dtype = torch.int32 if use_int32 else torch.int64
    alignment_heads = torch.ones((num_alignment_heads, 2), device=device, dtype=torch_dtype)
    return alignment_heads

