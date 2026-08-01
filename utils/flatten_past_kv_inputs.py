
def flatten_past_kv_inputs(past_key_values: list[tuple[torch.Tensor, torch.Tensor]]):
    past_kv = {}
    for i, (past_k, past_v) in enumerate(past_key_values):
        if isinstance(past_key_values, DynamicCache):
            past_kv[f"past_key_values_key_cache_{i}"] = past_k.detach().cpu().numpy()
            past_kv[f"past_key_values_value_cache_{i}"] = past_v.detach().cpu().numpy()
        else:
            past_kv[f"past_key_values.{i}.key"] = past_k.detach().cpu().numpy()
            past_kv[f"past_key_values.{i}.value"] = past_v.detach().cpu().numpy()
    return past_kv

