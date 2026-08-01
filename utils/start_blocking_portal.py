
def start_blocking_portal(
    backend: str = "asyncio",
    backend_options: dict[str, Any] | None = None,
    *,
    name: str | None = None,
) -> Generator[BlockingPortal, Any, None]:
    """
    Start a new event loop in a new thread and run a blocking portal in its main task.

    The parameters are the same as for :func:`~anyio.run`.

    :param backend: name of the backend
    :param backend_options: backend options
    :param name: name of the thread
    :return: a context manager that yields a blocking portal

    .. versionchanged:: 3.0
        Usage as a context manager is now required.

    """

    async def run_portal() -> None:
        async with BlockingPortal() as portal_:
            if name is None:
                current_thread().name = f"{backend}-portal-{id(portal_):x}"

            future.set_result(portal_)
            await portal_.sleep_until_stopped()

    def run_blocking_portal() -> None:
        if future.set_running_or_notify_cancel():
            try:
                run_eventloop(
                    run_portal, backend=backend, backend_options=backend_options
                )
            except BaseException as exc:
                if not future.done():
                    future.set_exception(exc)

    future: Future[BlockingPortal] = Future()
    thread = Thread(target=run_blocking_portal, daemon=True, name=name)
    thread.start()
    try:
        cancel_remaining_tasks = False
        portal = future.result()
        try:
            yield portal
        except BaseException:
            cancel_remaining_tasks = True
            raise
        finally:
            try:
                portal.call(portal.stop, cancel_remaining_tasks)
            except RuntimeError:
                pass
    finally:
        thread.join()

