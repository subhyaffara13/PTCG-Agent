
def get_sample_jump_times_inputs(
    config: WhisperConfig,
    device: torch.device,
    batch_size: int,
    sequence_length: int,
    num_alignment_heads: int,
    sot_sequence_length: int,
    segment_length: int,
    use_fp16: bool = False,
    use_int32: bool = True,
):
    alignment_heads = get_sample_alignment_heads(config, device, num_alignment_heads, use_int32)
    # lengths need to be int64 because subsequent 'Slice' ops only take int64 inputs
    sot_sequence_length = get_sample_sot_sequence_length(device, sot_sequence_length)
    segment_length = get_sample_segment_length(device, segment_length)
    QKs = get_sample_QKs(config, device, batch_size, sequence_length, use_fp16)  # noqa: N806
    return {
        "alignment_heads": alignment_heads,
        "sot_sequence_length": sot_sequence_length,
        "segment_length": segment_length,
        "QKs": QKs,
    }

