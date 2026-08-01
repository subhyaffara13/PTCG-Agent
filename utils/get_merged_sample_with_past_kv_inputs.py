
def get_merged_sample_with_past_kv_inputs(
    config: AutoConfig,
    device: torch.device,
    batch_size: int,
    seq_len: int,
    past_seq_len: int,
    max_seq_len: int,
    use_fp16: bool = False,
    use_buffer_share: bool = False,
    engine: str = "pt",
    return_dict: bool = False,
    world_size: int = 1,
):
    input_ids = torch.randint(low=0, high=config.vocab_size, size=(batch_size, seq_len), dtype=torch.int64)
    attention_mask = torch.ones(batch_size, past_seq_len + seq_len, dtype=torch.int64)
    # position_ids is of shape (batch_size, seq_len) for prompt generation, (batch_size, 1) for token generation
    position_ids = get_position_ids(attention_mask, use_past_kv=(past_seq_len != 0))
    past_kv = get_past_kv_inputs(config, batch_size, past_seq_len, use_fp16, world_size=world_size)

    # Convert inputs to NumPy (for ORT) or send to device (for PyTorch)
    input_ids = input_ids.numpy() if engine == "ort" else input_ids.to(device)
    attention_mask = attention_mask.numpy() if engine == "ort" else attention_mask.to(device)
    position_ids = position_ids.numpy() if engine == "ort" else position_ids.to(device)
    past_kv = (
        flatten_past_kv_inputs(past_kv) if engine == "ort" else [(kv[0].to(device), kv[1].to(device)) for kv in past_kv]
    )

    if not return_dict:
        # For export
        assert isinstance(past_kv, list)
        return (input_ids, attention_mask, position_ids, past_kv)

    inputs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "position_ids": position_ids,
    }
    if engine == "ort":
        assert isinstance(past_kv, dict)
        inputs.update(past_kv)

        if use_buffer_share:
            inputs = enable_past_present_share_buffer(inputs, past_seq_len, max_seq_len)

    else:
        assert isinstance(past_kv, list)
        inputs["past_key_values"] = past_kv

    return inputs

