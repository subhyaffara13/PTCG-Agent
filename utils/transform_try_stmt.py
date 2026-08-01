
def transform_try_stmt(builder: IRBuilder, t: TryStmt) -> None:
    # Our compilation strategy for try/except/else/finally is to
    # treat try/except/else and try/finally as separate language
    # constructs that we compile separately. When we have a
    # try/except/else/finally, we treat the try/except/else as the
    # body of a try/finally block.
    if t.is_star:
        builder.error("Exception groups and except* cannot be compiled yet", t.line)

    # Check if we're in an async function with a finally block that contains await
    use_async_version = False
    if t.finally_body and builder.fn_info.is_coroutine:
        detector = AwaitDetector()
        t.finally_body.accept(detector)

        if detector.has_await:
            # Use the async version that handles exceptions correctly
            use_async_version = True

    if t.finally_body:

        def transform_try_body() -> None:
            if t.handlers:
                transform_try_except_stmt(builder, t)
            else:
                builder.accept(t.body)

        body = t.finally_body

        if use_async_version:
            transform_try_finally_stmt_async(
                builder, transform_try_body, lambda: builder.accept(body), t.line
            )
        else:
            transform_try_finally_stmt(
                builder, transform_try_body, lambda: builder.accept(body), t.line
            )
    else:
        transform_try_except_stmt(builder, t)

