
def sync(loop, func, *args, timeout=None, **kwargs):
    """
    Make loop run coroutine until it returns. Runs in other thread

    Examples
    --------
    >>> fsspec.asyn.sync(fsspec.asyn.get_loop(), func, *args,
                         timeout=timeout, **kwargs)
    """
    timeout = timeout if timeout else None  # convert 0 or 0.0 to None
    # NB: if the loop is not running *yet*, it is OK to submit work
    # and we will wait for it
    if loop is None or loop.is_closed():
        raise RuntimeError("Loop is not running")
    try:
        loop0 = asyncio.events.get_running_loop()
        if loop0 is loop:
            raise NotImplementedError("Calling sync() from within a running loop")
    except NotImplementedError:
        raise
    except RuntimeError:
        pass
    coro = func(*args, **kwargs)
    result = [None]
    event = threading.Event()
    asyncio.run_coroutine_threadsafe(_runner(event, coro, result, timeout), loop)
    while True:
        # this loops allows thread to get interrupted
        if event.wait(1):
            break
        if timeout is not None:
            timeout -= 1
            if timeout < 0:
                raise FSTimeoutError

    return_result = result[0]
    if isinstance(return_result, asyncio.TimeoutError):
        # suppress asyncio.TimeoutError, raise FSTimeoutError
        raise FSTimeoutError from return_result
    elif isinstance(return_result, BaseException):
        raise return_result
    else:
        return return_result


def sync(
    source: Annotated[
        str | None,
        typer.Argument(
            help="Source path: local directory or hf://buckets/namespace/bucket_name(/prefix)",
        ),
    ] = None,
    dest: Annotated[
        str | None,
        typer.Argument(
            help="Destination path: local directory or hf://buckets/namespace/bucket_name(/prefix)",
        ),
    ] = None,
    delete: Annotated[
        bool,
        typer.Option(
            help="Delete destination files not present in source.",
        ),
    ] = False,
    ignore_times: Annotated[
        bool,
        typer.Option(
            "--ignore-times",
            help="Skip files only based on size, ignoring modification times.",
        ),
    ] = False,
    ignore_sizes: Annotated[
        bool,
        typer.Option(
            "--ignore-sizes",
            help="Skip files only based on modification times, ignoring sizes.",
        ),
    ] = False,
    plan: Annotated[
        str | None,
        typer.Option(
            help="Save sync plan to JSONL file for review instead of executing.",
        ),
    ] = None,
    apply: Annotated[
        str | None,
        typer.Option(
            help="Apply a previously saved plan file.",
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Print sync plan to stdout as JSONL without executing.",
        ),
    ] = False,
    include: Annotated[
        list[str] | None,
        typer.Option(
            help="Include files matching pattern (can specify multiple).",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            help="Exclude files matching pattern (can specify multiple).",
        ),
    ] = None,
    filter_from: Annotated[
        str | None,
        typer.Option(
            help="Read include/exclude patterns from file.",
        ),
    ] = None,
    existing: Annotated[
        bool,
        typer.Option(
            "--existing",
            help="Skip creating new files on receiver (only update existing files).",
        ),
    ] = False,
    ignore_existing: Annotated[
        bool,
        typer.Option(
            "--ignore-existing",
            help="Skip updating files that exist on receiver (only create new files).",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Show detailed logging with reasoning.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Sync files between local directory and a bucket."""
    api = get_hf_api(token=token)
    api.sync_bucket(
        source=source,
        dest=dest,
        delete=delete,
        ignore_times=ignore_times,
        ignore_sizes=ignore_sizes,
        existing=existing,
        ignore_existing=ignore_existing,
        include=include,
        exclude=exclude,
        filter_from=filter_from,
        plan=plan,
        apply=apply,
        dry_run=dry_run,
        verbose=verbose,
        quiet=out.is_quiet(),
    )
    if plan and not out.is_quiet():
        out.hint(f"Run `hf buckets sync --apply {plan}` to execute this plan.")

