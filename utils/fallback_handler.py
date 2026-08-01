
def fallback_handler(kernel, add_to_fallback_set=True):
    if add_to_fallback_set:
        fallbacks.add(kernel)

    def handler(*args, **kwargs):
        def wrap_tensors(x):
            return x.wrap_for_lowering() if isinstance(x, ir.IRNode) else x

        return pytree.tree_map(
            wrap_tensors, ir.FallbackKernel.create(kernel, *args, **kwargs)
        )

    # This lets us detect that a lowering is a fallback handler.
    handler._is_fallback_handler = True  # type: ignore[attr-defined]

    return handler

