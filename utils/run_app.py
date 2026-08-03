import logging
from typing import Any, Callable

def run_app(
    app: Application | Awaitable[Application],
    *,
    host: str | HostSequence | None = None,
    port: int | None = None,
    path: PathLike | TypingIterable[PathLike] | None = None,
    sock: socket.socket | TypingIterable[socket.socket] | None = None,
    shutdown_timeout: float = 60.0,
    keepalive_timeout: float = 75.0,
    ssl_context: SSLContext | None = None,
    print: Callable[..., None] | None = print,
    backlog: int = 128,
    access_log_class: type[AbstractAccessLogger] = AccessLogger,
    access_log_format: str = AccessLogger.LOG_FORMAT,
    access_log: logging.Logger | None = access_logger,
    handle_signals: bool = True,
    reuse_address: bool | None = None,
    reuse_port: bool | None = None,
    handler_cancellation: bool = False,
    loop: asyncio.AbstractEventLoop | None = None,
    **kwargs: Any,
) -> None:
    """Run an app locally"""
    if loop is None:
        loop = asyncio.new_event_loop()

    # Configure if and only if in debugging mode and using the default logger
    if loop.get_debug() and access_log and access_log.name == "aiohttp.access":
        if access_log.level == logging.NOTSET:
            access_log.setLevel(logging.DEBUG)
        if not access_log.hasHandlers():
            access_log.addHandler(logging.StreamHandler())

    main_task = loop.create_task(
        _run_app(
            app,
            host=host,
            port=port,
            path=path,
            sock=sock,
            shutdown_timeout=shutdown_timeout,
            keepalive_timeout=keepalive_timeout,
            ssl_context=ssl_context,
            print=print,
            backlog=backlog,
            access_log_class=access_log_class,
            access_log_format=access_log_format,
            access_log=access_log,
            handle_signals=handle_signals,
            reuse_address=reuse_address,
            reuse_port=reuse_port,
            handler_cancellation=handler_cancellation,
            **kwargs,
        )
    )

    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main_task)
    except (GracefulExit, KeyboardInterrupt):  # pragma: no cover
        pass
    finally:
        try:
            # Skip when ``main_task`` is already done (e.g. raised during startup).
            # Re-running ``loop.run_until_complete`` on a finished task calls
            # ``Future.result`` again, which does
            # ``raise self._exception.with_traceback(self._exception_tb)`` and
            # resets ``exc.__traceback__`` to the originally saved tb — by then
            # shallow — clobbering the deep traceback the caller would otherwise
            # see (frames from ``cleanup_ctx`` / ``on_startup`` and the user code
            # that actually raised).
            if not main_task.done():
                main_task.cancel()
                with suppress(asyncio.CancelledError):
                    loop.run_until_complete(main_task)
        finally:
            _cancel_tasks(asyncio.all_tasks(loop), loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

