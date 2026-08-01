
def use_group_query_attention(config: AutoConfig, model_opt: OnnxModel, world_size: int = 1, window_size: int = -1):
    # Replace MultiHeadAttention with GroupQueryAttention
    model_opt = replace_mha_with_gqa(model_opt, "attention_mask", config.num_key_value_heads, world_size, window_size)
    model_opt.prune_graph()
    model_opt.update_graph(allow_remove_graph_inputs=True)
    return model_opt

