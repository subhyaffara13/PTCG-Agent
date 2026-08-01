
def get_sample_encoder_hidden_states(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    use_fp16: bool = False,
):
    torch_dtype = torch.float16 if use_fp16 else torch.float32
    encoder_hidden_states = torch.randn(
        batch_size, config.max_source_positions, config.d_model, device=device, dtype=torch_dtype
    )
    return encoder_hidden_states

