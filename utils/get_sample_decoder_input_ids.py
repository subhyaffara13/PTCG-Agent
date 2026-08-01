
def get_sample_decoder_input_ids(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    sequence_length: int,
    use_int32: bool = True,
):
    torch_dtype = torch.int32 if use_int32 else torch.int64
    decoder_input_ids = torch.randint(
        low=0, high=config.vocab_size, size=(batch_size, sequence_length), device=device, dtype=torch_dtype
    )
    return decoder_input_ids

