
def get_sample_past_key_values(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    past_seq_len: int,
    use_fp16: bool = False,
):
    num_heads = config.decoder_attention_heads
    head_size = config.d_model // num_heads
    max_source_positions = (
        config.max_source_positions
    )  # equal to num_frames // 2 = encoder's sequence_length // 2 = 3000 // 2 = 1500
    torch_dtype = torch.float16 if use_fp16 else torch.float32
    self_attention_kv_caches = [
        (
            torch.rand(batch_size, num_heads, past_seq_len, head_size, device=device, dtype=torch_dtype),
            torch.rand(batch_size, num_heads, past_seq_len, head_size, device=device, dtype=torch_dtype),
        )
        for _ in range(config.decoder_layers)
    ]
    cross_attention_kv_caches = [
        (
            torch.rand(batch_size, num_heads, max_source_positions, head_size, device=device, dtype=torch_dtype),
            torch.rand(batch_size, num_heads, max_source_positions, head_size, device=device, dtype=torch_dtype),
        )
        for _ in range(config.decoder_layers)
    ]
    return flatten_past_key_values(self_attention_kv_caches, cross_attention_kv_caches)

