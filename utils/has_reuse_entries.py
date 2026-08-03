from typing import Any

def has_reuse_entries(
    tx: "InstructionTranslator",
    fn_var: Any,
) -> bool:
    """Cheap check: does the cache have any entries for this function?"""
    from torch._guards import InvokeSubgraphCache

    invoke_subgraph_cache = tx.output.tracing_context.hop_dispatch_set_cache.get_cache(
        torch._higher_order_ops.invoke_subgraph
    )
    if not isinstance(invoke_subgraph_cache, InvokeSubgraphCache):
        return False
    fn_code = get_fn_code(fn_var)
    return fn_code is not None and fn_code in invoke_subgraph_cache.subgraph_reuse_cache

