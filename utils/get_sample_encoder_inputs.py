
def get_sample_encoder_inputs(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    sequence_length: int = 3000,
    use_fp16: bool = False,
):
    audio_features = get_sample_audio_features(config, device, batch_size, sequence_length, use_fp16)
    return {"audio_features": audio_features}

