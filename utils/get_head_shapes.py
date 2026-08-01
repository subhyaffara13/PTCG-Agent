
def get_head_shapes(config) -> tuple[int | list[int], int | list[int]]:
    """Returns a tuple `(num_heads, head_dim)` containing either 2 ints, or a list of int with the value for each
    layer."""
    # Gemma4 has different head_dim and num_heads depending on layer type
    if hasattr(config, "global_head_dim"):
        head_dim = [
            config.global_head_dim if layer == "full_attention" else config.head_dim
            for layer in config.layer_types[: -config.num_kv_shared_layers]
        ]
        num_heads = [
            config.num_global_key_value_heads
            if layer == "full_attention" and config.attention_k_eq_v
            else config.num_key_value_heads
            for layer in config.layer_types[: -config.num_kv_shared_layers]
        ]
    else:
        head_dim = getattr(config, "head_dim", config.hidden_size // config.num_attention_heads)
        num_heads = getattr(config, "num_key_value_heads", config.num_attention_heads)

    return num_heads, head_dim

