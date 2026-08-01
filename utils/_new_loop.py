
def _new_loop(
    task_factory: TaskFactoryType | None = None,
) -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    tasks = _patch_loop(loop)

    if task_factory:
        # pyre-ignore[6]
        loop.set_task_factory(task_factory)  # type: ignore[arg-type]

    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        try:
            _cancel_all_tasks(loop, tasks)
        finally:
            asyncio.set_event_loop(None)
            loop.close()

