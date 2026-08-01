
def _grouped_mm_fallback_setup_context(ctx, inputs, output):
    """Saves input and weight for backward; offs is stored directly as it is a non-differentiable integer tensor."""
    ctx.save_for_backward(inputs[0], inputs[1])
    ctx.offs = inputs[2]

