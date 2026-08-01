
def get_sample_decoder_inputs(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    past_sequence_length: int,
    sequence_length: int,
    use_fp16: bool = False,
    use_int32: bool = True,
):
    decoder_input_ids = get_sample_decoder_input_ids(config, device, batch_size, sequence_length, use_int32)
    encoder_hidden_states = get_sample_encoder_hidden_states(config, device, batch_size, use_fp16)
    past_key_values = get_sample_past_key_values(config, device, batch_size, past_sequence_length, use_fp16)
    return {
        "decoder_input_ids": decoder_input_ids,
        "encoder_hidden_states": encoder_hidden_states,
        "past_key_values": past_key_values,
    }

