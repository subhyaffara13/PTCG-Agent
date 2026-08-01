
def clear_lru_cache() -> None:
    torch._dynamo.trace_rules.get_torch_obj_rule_map.cache_clear()
    torch._dynamo.trace_rules.get_tensor_method.cache_clear()
    torch._dynamo.trace_rules.get_legacy_mod_inlinelist.cache_clear()
    torch._dynamo.trace_rules.get_mod_inlinelist.cache_clear()
    torch._dynamo.trace_rules.dynamo_dir.cache_clear()

