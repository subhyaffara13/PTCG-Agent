
def disallow_side_effects_in_generator(
    tx: "InstructionTranslatorBase",
) -> Generator[None, None, None]:
    orig_val = tx.output.current_tracer.is_reconstructing_generator
    try:
        tx.output.current_tracer.is_reconstructing_generator = True
        yield
    finally:
        tx.output.current_tracer.is_reconstructing_generator = orig_val

