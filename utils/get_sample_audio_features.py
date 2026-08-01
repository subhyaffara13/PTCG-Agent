
def get_sample_audio_features(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    sequence_length: int = 3000,
    use_fp16: bool = False,
):
    torch_dtype = torch.float16 if use_fp16 else torch.float32
    audio_features = torch.randn(batch_size, config.num_mel_bins, sequence_length, device=device, dtype=torch_dtype)
    return audio_features

