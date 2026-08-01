
def find_reuse_match(
    tx: "InstructionTranslator",
    fn_var: Any,
    fingerprint: InputFingerprint,
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

    # this evaluator function is called one by one for all the invoke subgraph
    # reuse entries - the one that evaluates to True is stamped out in the
    # graph.
    def evaluator(
        cond: "InvokeSubgraphReuseCondition", entry: InvokeSubgraphReuseEntry
    ) -> bool:
        return is_reusable(tx, cond, fingerprint, entry)

    return invoke_subgraph_cache.find_reuse_entry(fn_code, evaluator)

