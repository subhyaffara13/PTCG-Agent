
def allow_side_effects_in_hop(
    tx: "InstructionTranslatorBase",
) -> Generator[None, None, None]:
    """Context manager to temporarily allow side effects with extra outputs.

    This is used for special cases (like FSDP functions) that need to perform
    side effects even when the general policy is to disallow them.
    """
    orig_val = tx.output.current_tracer.allow_side_effects_in_hop
    try:
        tx.output.current_tracer.allow_side_effects_in_hop = True
        yield
    finally:
        tx.output.current_tracer.allow_side_effects_in_hop = orig_val

