
def get_past_kv_inputs(config: AutoConfig, batch_size: int, past_seq_len: int, use_fp16: bool, world_size: int = 1):
    num_heads = config.num_key_value_heads // world_size
    head_size = config.head_dim if hasattr(config, "head_dim") else config.hidden_size // config.num_attention_heads
    torch_dtype = torch.float16 if use_fp16 else torch.float32
    past_kv = [
        (
            torch.rand(batch_size, num_heads, past_seq_len, head_size, dtype=torch_dtype),
            torch.rand(batch_size, num_heads, past_seq_len, head_size, dtype=torch_dtype),
        )
        for _ in range(config.num_hidden_layers)
    ]
    return past_kv

