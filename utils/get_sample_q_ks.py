
def get_sample_QKs(  # noqa: N802
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    sequence_length: int,
    use_fp16: bool = False,
):
    num_heads = config.decoder_attention_heads
    torch_dtype = torch.float16 if use_fp16 else torch.float32
    QKs = [  # noqa: N806
        torch.rand(
            batch_size, num_heads, sequence_length, config.max_source_positions, device=device, dtype=torch_dtype
        )
        for _ in range(config.decoder_layers)
    ]
    return QKs

