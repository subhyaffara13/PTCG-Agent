
def get_msft_sample_inputs(
    config: AutoConfig,
    batch_size: int,
    past_seq_len: int,
    seq_len: int,
    max_seq_len: int,
    use_fp16: bool,
    use_buffer_share: bool,
    split_kv: bool,
):
    np_dtype = np.float16 if use_fp16 else np.float32
    head_size = config.hidden_size // config.num_attention_heads

    if not split_kv:
        ort_inputs = {
            "x": np.random.rand(batch_size, seq_len, config.hidden_size).astype(np_dtype),
            "attn_mask": (-10000.0 * np.triu(np.ones((batch_size, max_seq_len, max_seq_len)), k=1)).astype(np_dtype),
            "k_cache": np.random.rand(
                batch_size, config.num_hidden_layers, past_seq_len, config.num_attention_heads, head_size
            ).astype(np_dtype),
            "v_cache": np.random.rand(
                batch_size, config.num_hidden_layers, past_seq_len, config.num_attention_heads, head_size
            ).astype(np_dtype),
            "pos": np.array(past_seq_len, dtype=np.int64),
        }
    else:
        ort_inputs = {
            "x": np.random.rand(batch_size, seq_len, config.hidden_size).astype(np_dtype),
            "attn_mask": (np.triu(np.ones((batch_size, max_seq_len, max_seq_len), dtype=np.int32), k=1) - 1).astype(
                np.int32
            ),
            "pos": np.array(past_seq_len, dtype=np.int64),
        }
        for i in range(config.num_hidden_layers):
            ort_inputs.update(
                {
                    f"k_{i}_cache": np.random.rand(
                        batch_size, config.num_attention_heads, past_seq_len, head_size
                    ).astype(np_dtype),
                    f"v_{i}_cache": np.random.rand(
                        batch_size, config.num_attention_heads, past_seq_len, head_size
                    ).astype(np_dtype),
                }
            )

        if use_buffer_share:
            ort_inputs = enable_past_present_share_buffer(ort_inputs, past_seq_len, max_seq_len)

    return ort_inputs

