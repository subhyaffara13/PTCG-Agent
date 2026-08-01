
def get_dummy_inputs(config, export_padding, device):
    # When sequence length is multiple of windows size, there is no padding logic in ONNX graph
    sequence_length = config.attention_window[0] + 1 if export_padding else config.attention_window[0]

    # Create dummy inputs
    input_ids = torch.arange(sequence_length).unsqueeze(0).to(device)

    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=device)
    attention_mask[:, sequence_length - 1] = 0  # last token is masked

    global_attention_mask = torch.zeros(input_ids.shape, dtype=torch.long, device=device)
    global_attention_mask[:, 0] = 1  # first token is global token

    return input_ids, attention_mask, global_attention_mask

