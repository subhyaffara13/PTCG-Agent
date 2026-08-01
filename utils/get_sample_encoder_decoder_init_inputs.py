
def get_sample_encoder_decoder_init_inputs(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    decoder_sequence_length: int,
    encoder_sequence_length: int = 3000,
    use_fp16: bool = False,
    use_int32: bool = True,
):
    audio_features = get_sample_audio_features(config, device, batch_size, encoder_sequence_length, use_fp16)
    decoder_input_ids = get_sample_decoder_input_ids(config, device, batch_size, decoder_sequence_length, use_int32)
    return {"audio_features": audio_features, "decoder_input_ids": decoder_input_ids}

