
def find_reuse_entry_by_key(
    tx: "InstructionTranslator",
    fn_var: Any,
    hash_key: int,
) -> InvokeSubgraphReuseEntry | None:
    from torch._guards import InvokeSubgraphCache

    invoke_subgraph_cache = tx.output.tracing_context.hop_dispatch_set_cache.get_cache(
        torch._higher_order_ops.invoke_subgraph
    )
    if not isinstance(invoke_subgraph_cache, InvokeSubgraphCache):
        return None
    fn_code = get_fn_code(fn_var)
    if fn_code is None:
        return None
    return invoke_subgraph_cache.find_reuse_entry_by_key(fn_code, hash_key)

