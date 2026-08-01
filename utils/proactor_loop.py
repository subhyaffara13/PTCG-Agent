
def proactor_loop() -> Iterator[asyncio.AbstractEventLoop]:
    factory = asyncio.ProactorEventLoop  # type: ignore[attr-defined]

    with loop_context(factory) as _loop:
        asyncio.set_event_loop(_loop)
        yield _loop

