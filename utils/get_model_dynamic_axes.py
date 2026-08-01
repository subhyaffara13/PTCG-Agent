
def get_model_dynamic_axes(input_names: list[str], output_names: list[str]):
    dynamic_axes = {}
    for name in input_names + output_names:
        if name in input_names:
            # shape is (batch_size, sequence_length)
            dynamic_axes[name] = {0: "batch_size", 1: "sequence_length"}
        elif name == "logits":
            # shape is (batch_size, sequence_length, vocab_size)
            dynamic_axes[name] = {0: "batch_size", 1: "sequence_length"}
        elif "present" in name:
            # shape is (batch_size, num_heads, sequence_length, head_size)
            dynamic_axes[name] = {0: "batch_size", 2: "sequence_length"}
        else:
            raise Exception("Unknown input or output name found")
    return dynamic_axes


def get_model_dynamic_axes(
    config: WhisperConfig,
    input_names: list[str],
    output_names: list[str],
):
    dynamic_axes = {}
    for name in input_names + output_names:
        if name in {"audio_features", "encoder_input_ids"}:
            # shape is (batch_size, num_mels, num_frames)
            dynamic_axes[name] = {0: "batch_size"}
        elif name in {"input_ids", "decoder_input_ids"}:
            # shape is (batch_size, sequence_length)
            dynamic_axes[name] = {0: "batch_size", 1: "sequence_length"}
        elif name == "alignment_heads":
            # shape is (num_alignment_heads, 2)
            dynamic_axes[name] = {0: "num_alignment_heads"}
        elif name in {"sot_sequence_length", "segment_length"}:
            # shape is (1)
            pass
        elif name == "logits":
            # shape is (batch_size, sequence_length, vocab_size)
            dynamic_axes[name] = {0: "batch_size", 1: "sequence_length"}
        elif name == "encoder_hidden_states":
            # shape is (batch_size, num_frames // 2, hidden_size)
            dynamic_axes[name] = {0: "batch_size"}
        elif "past_key_self" in name or "past_value_self" in name:
            # shape is (batch_size, num_heads, past_sequence_length, head_size)
            dynamic_axes[name] = {0: "batch_size", 2: "past_sequence_length"}
        elif "present_key_self" in name or "present_value_self" in name:
            # shape is (batch_size, num_heads, past_sequence_length + sequence_length, head_size),
            # which is equal to (batch_size, num_heads, total_sequence_length, head_size)
            dynamic_axes[name] = {0: "batch_size", 2: "total_sequence_length"}
        elif (
            "past_key_cross" in name
            or "past_value_cross" in name
            or "present_key_cross" in name
            or "present_value_cross" in name
        ):
            # shape is (batch_size, num_heads, num_frames // 2, head_size)
            dynamic_axes[name] = {0: "batch_size"}
        elif "cross_qk" in name:
            # shape is (batch_size, num_heads, source_sequence_length, target_sequence_length)
            dynamic_axes[name] = {0: "batch_size", 2: "sequence_length"}
        elif "jump_times" in name:
            # shape is (batch_size, max_length)
            dynamic_axes[name] = {0: "batch_size", 1: "max_length"}
        else:
            raise Exception(f"Unknown input or output name found: {name}")
    return dynamic_axes

