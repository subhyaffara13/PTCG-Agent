
def flatten_past_key_values(
    self_attn_kv_caches: list[tuple[torch.Tensor, torch.Tensor]],
    cross_attn_kv_caches: list[tuple[torch.Tensor, torch.Tensor]],
):
    past_key_values = []
    for (self_k_cache, self_v_cache), (cross_k_cache, cross_v_cache) in zip(
        self_attn_kv_caches, cross_attn_kv_caches, strict=False
    ):
        layer_kv_caches = (self_k_cache, self_v_cache, cross_k_cache, cross_v_cache)
        past_key_values.append(layer_kv_caches)
    return past_key_values

