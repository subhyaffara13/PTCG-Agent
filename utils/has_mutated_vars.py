
def has_mutated_vars(
    tx: "InstructionTranslator",
    traced_sources: OrderedSet[Source],
) -> bool:
    """Check if any source accessed by the subgraph has been mutated.

    SideEffects.mutated_sources records the exact AttrSource for every
    store_attr call. A simple set intersection with traced_sources tells
    us whether any source the subgraph read was later written to.
    """
    overlap = tx.output.side_effects.mutated_sources & traced_sources
    if overlap:
        hc_log.debug(
            "subgraph_reuse: mutated sources detected -- %s",
            overlap,
        )
        return True
    return False

