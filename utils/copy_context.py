
def copy_context(context: InferenceContext | None) -> InferenceContext:
    """Clone a context if given, or return a fresh context."""
    if context is not None:
        return context.clone()

    return InferenceContext()

