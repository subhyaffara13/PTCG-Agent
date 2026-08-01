
def get_loop():
    """Create or return the default fsspec IO loop

    The loop will be running on a separate thread.
    """
    if loop[0] is None:
        with get_lock():
            # repeat the check just in case the loop got filled between the
            # previous two calls from another thread
            if loop[0] is None:
                loop[0] = asyncio.new_event_loop()
                th = threading.Thread(target=loop[0].run_forever, name="fsspecIO")
                th.daemon = True
                th.start()
                iothread[0] = th
    return loop[0]


def get_loop(
    always_create_new_loop: bool = False,
) -> Iterator[AbstractEventLoop]:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as re:
        if "There is no current event loop in thread" in str(re):
            with _new_loop() as loop:
                yield loop
            return
        else:
            raise

    @contextmanager
    def _restore_loop(
        loop: asyncio.AbstractEventLoop,
    ) -> Iterator[None]:
        try:
            yield
        finally:
            asyncio.set_event_loop(loop)

    @contextmanager
    def _restore_running_loop() -> Iterator[None]:
        loop_from_events = asyncio.events._get_running_loop()
        asyncio.events._set_running_loop(None)
        try:
            yield
        finally:
            asyncio.events._set_running_loop(loop_from_events)

    with ExitStack() as stack:
        if loop.is_running():
            stack.enter_context(_restore_running_loop())
            stack.enter_context(_restore_loop(loop=loop))
            loop = stack.enter_context(_new_loop(loop.get_task_factory()))  # type: ignore[arg-type]
        elif loop.is_closed():
            loop = stack.enter_context(_new_loop())  # type: ignore[arg-type]
        elif always_create_new_loop:
            stack.enter_context(_restore_loop(loop=loop))
            loop = stack.enter_context(_new_loop())  # type: ignore[arg-type]
        yield loop

