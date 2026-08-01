
def get_sample_inputs(
    config: AutoConfig,
    device: torch.device,
    batch_size: int,
    seq_len: int,
    engine: str = "pt",
    return_dict: bool = False,
):
    input_ids = torch.randint(low=0, high=config.vocab_size, size=(batch_size, seq_len), dtype=torch.int64)
    attention_mask = torch.ones(batch_size, seq_len, dtype=torch.int64)
    position_ids = get_position_ids(attention_mask, use_past_kv=False)

    # Convert inputs to NumPy (for ORT) or send to device (for PyTorch)
    input_ids = input_ids.numpy() if engine == "ort" else input_ids.to(device)
    attention_mask = attention_mask.numpy() if engine == "ort" else attention_mask.to(device)
    position_ids = position_ids.numpy() if engine == "ort" else position_ids.to(device)

    if not return_dict:
        # For export
        return (input_ids, attention_mask, position_ids)

    inputs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "position_ids": position_ids,
    }
    return inputs

