
def reset_code_caches() -> None:
    """
    Clears in-memory code cache, which is what stores compiled products.  This
    resets less state than :func:`reset` and is mostly only used for testing
    purposes.
    """
    # TODO: https://github.com/pytorch/pytorch/issues/139200
    import logging

    log = logging.getLogger(__name__)
    log.info("torch._dynamo.reset_code_caches")
    """Clear compile caches that are keyed by code objects"""
    with convert_frame.compile_lock:
        reset_code_state()
        for weak_code in (
            convert_frame.input_codes.seen + convert_frame.output_codes.seen
        ):
            code = weak_code()
            if code:
                reset_code(code)
        code_context.clear()

