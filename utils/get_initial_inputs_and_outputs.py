
def get_initial_inputs_and_outputs(
    config: AutoConfig,
    tokenizer: AutoTokenizer,
    requested_length: int,
    prompt: list[str],
    device: torch.device,
    use_fp16: bool,
    use_buffer_share: bool,
    engine: str,
):
    tokenizer.pad_token = tokenizer.eos_token
    encodings_dict = tokenizer.batch_encode_plus(prompt, padding=True)
    torch_dtype = torch.float16 if use_fp16 else torch.float32

    # input_ids:      pad token id is 0
    # attention_mask: pad token id is 0
    # position_ids:   pad token id is 1
    input_ids = torch.tensor(encodings_dict["input_ids"], device=device, dtype=torch.int64)
    attention_mask = torch.tensor(encodings_dict["attention_mask"], device=device, dtype=torch.int64)
    position_ids = get_position_ids(attention_mask, use_past_kv=False)

    # Check if tokenized prompt length matches the requested prompt length
    tokenized_length = input_ids.shape[-1]
    if tokenized_length > requested_length:
        # Shorten the inputs from (batch_size, tokenized_length) to (batch_size, requested_length)
        input_ids = input_ids[:, :requested_length]
        attention_mask = attention_mask[:, :requested_length]
        position_ids = get_position_ids(attention_mask, use_past_kv=False)
    elif tokenized_length < requested_length:
        # Lengthen the inputs from (batch_size, tokenized_length) to (batch_size, requested_length)
        input_ids_first_col = input_ids[:, 0].unsqueeze(0).T
        attention_mask_first_col = attention_mask[:, 0].unsqueeze(0).T
        for _ in range(requested_length - tokenized_length):
            input_ids = torch.hstack((input_ids_first_col, input_ids))
            attention_mask = torch.hstack((attention_mask_first_col, attention_mask))
        position_ids = get_position_ids(attention_mask, use_past_kv=False)

    tokenized_length = input_ids.shape[-1]
    assert tokenized_length == requested_length

    # Create inputs
    inputs = {
        "input_ids": input_ids.contiguous() if engine == "ort" else input_ids,
        "attention_mask": attention_mask.contiguous() if engine == "ort" else attention_mask,
        "position_ids": position_ids.contiguous() if engine == "ort" else position_ids,
    }
    if engine != "ort":
        inputs["past_key_values"] = []

    # Get shape of KV cache inputs
    batch_size, sequence_length = input_ids.shape
    max_sequence_length = config.max_position_embeddings
    num_heads = config.num_key_value_heads
    head_size = config.head_dim if hasattr(config, "head_dim") else config.hidden_size // config.num_attention_heads

    # Create KV cache inputs
    for i in range(config.num_hidden_layers):
        past_key = torch.zeros(
            batch_size,
            num_heads,
            max_sequence_length if use_buffer_share else 0,
            head_size,
            device=device,
            dtype=torch_dtype,
        )
        past_value = torch.zeros(
            batch_size,
            num_heads,
            max_sequence_length if use_buffer_share else 0,
            head_size,
            device=device,
            dtype=torch_dtype,
        )
        if engine == "ort":
            inputs.update(
                {
                    f"past_key_values.{i}.key": past_key.contiguous(),
                    f"past_key_values.{i}.value": past_value.contiguous(),
                }
            )
        else:
            inputs["past_key_values"].append((past_key, past_value))

    outputs = None
    if engine == "ort":
        # Create outputs
        logits = torch.zeros(batch_size, sequence_length, config.vocab_size, device=device, dtype=torch_dtype)
        outputs = {"logits": logits.contiguous()}
        if not use_buffer_share:
            for i in range(config.num_hidden_layers):
                present_key = torch.zeros(
                    batch_size, num_heads, sequence_length, head_size, device=device, dtype=torch_dtype
                )
                present_value = torch.zeros(
                    batch_size, num_heads, sequence_length, head_size, device=device, dtype=torch_dtype
                )
                outputs.update(
                    {f"present.{i}.key": present_key.contiguous(), f"present.{i}.value": present_value.contiguous()}
                )

    return inputs, outputs

