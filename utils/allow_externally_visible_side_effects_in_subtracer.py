
def allow_externally_visible_side_effects_in_subtracer(
    tx: "InstructionTranslatorBase",
) -> Generator[None, None, None]:
    orig_val = tx.output.current_tracer.unsafe_allow_externally_visible_side_effects
    try:
        tx.output.current_tracer.unsafe_allow_externally_visible_side_effects = True
        tx.output.current_tracer.traced_with_externally_visible_side_effects = True
        yield
    finally:
        tx.output.current_tracer.unsafe_allow_externally_visible_side_effects = orig_val

