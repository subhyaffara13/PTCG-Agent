
def inductor(*args: Any, **kwargs: Any) -> Any:
    with dynamo_timed("inductor_import", log_pt2_compile_event=True):
        # do import here to avoid loading inductor into memory when it is not used
        # The AsyncCompile subproc pool can be slow to start, so warm it up as early
        # as possible.
        from torch._inductor.async_compile import maybe_warm_pool

        maybe_warm_pool()

        from torch._inductor.compile_fx import compile_fx

    return compile_fx(*args, **kwargs)

