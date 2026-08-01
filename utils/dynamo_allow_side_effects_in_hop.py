
def dynamo_allow_side_effects_in_hop(
    tx: "InstructionTranslator",
) -> Generator[None, None, None]:
    orig_val = tx.output.current_tracer.allow_side_effects_in_hop
    try:
        tx.output.current_tracer.allow_side_effects_in_hop = True
        yield
    finally:
        tx.output.current_tracer.allow_side_effects_in_hop = orig_val

