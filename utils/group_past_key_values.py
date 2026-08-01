
def group_past_key_values(
    kv_caches: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]],
):
    self_attn_kv_caches, cross_attn_kv_caches = [], []
    for self_k_cache, self_v_cache, cross_k_cache, cross_v_cache in kv_caches:
        self_attn_kv_caches.append(self_k_cache)
        self_attn_kv_caches.append(self_v_cache)
        cross_attn_kv_caches.append(cross_k_cache)
        cross_attn_kv_caches.append(cross_v_cache)
    return self_attn_kv_caches, cross_attn_kv_caches

