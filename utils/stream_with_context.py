
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr],
) -> t.Iterator[t.AnyStr]: ...


def stream_with_context(
    generator_or_function: t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]: ...


def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

