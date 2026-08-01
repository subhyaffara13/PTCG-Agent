
def start_processes(
    fn,
    args=(),
    nprocs=1,
    join=True,
    daemon=False,
    start_method="spawn",
):
    # To speed up performance in certain cases (see https://github.com/pytorch/pytorch/issues/133010),
    # this func will start processes in parallel if start_method is 'forkserver'.
    # Please opt in to this perf optimization by setting env var (TORCH_MP_PARALLEL_START) to 1.
    # todo: investigate why spawn does not work with threadpool and raises SIGINT
    if (
        start_method == "forkserver"
        and os.environ.get(ENV_VAR_PARALLEL_START, "0") == "1"
    ):
        log.info("Starting processes in parallel.")
        start_parallel = True
    else:
        # Set env var TORCH_MP_PARALLEL_START to 0 to disable parallel start
        start_parallel = False

    mp = multiprocessing.get_context(start_method)
    error_files = [None] * nprocs
    processes = [None] * nprocs

    def start_process(i):
        # Each process is assigned a file to write tracebacks to.  We
        # use the file being non-empty to indicate an exception
        # occurred (vs an expected shutdown).  Note: this previously
        # used a multiprocessing.Queue but that can be prone to
        # deadlocks, so we went with a simpler solution for a one-shot
        # message between processes.
        tf = tempfile.NamedTemporaryFile(  # noqa: SIM115
            prefix="pytorch-errorfile-", suffix=".pickle", delete=False
        )
        tf.close()
        os.unlink(tf.name)

        process = mp.Process(  # pyrefly: ignore  # missing-attribute
            target=_wrap,
            args=(fn, i, args, tf.name),
            daemon=daemon,
        )

        process.start()
        return i, process, tf.name

    if not start_parallel:
        for i in range(nprocs):
            idx, process, tf_name = start_process(i)
            error_files[idx] = tf_name
            processes[idx] = process
    else:
        with ThreadPoolExecutor(max_workers=nprocs) as executor:
            futures = [executor.submit(start_process, i) for i in range(nprocs)]
            for fut in as_completed(futures):
                idx, process, tf_name = fut.result()
                # idx and process rank needs to be the same.
                error_files[idx] = tf_name
                processes[idx] = process
    context = ProcessContext(processes, error_files)
    if not join:
        return context

    # Loop on join until it returns True or raises an exception.
    while not context.join():
        pass


def start_processes(
    name: str,
    entrypoint: Callable | str,
    args: dict[int, tuple],
    envs: dict[int, dict[str, str]],
    logs_specs: LogsSpecs,
    log_line_prefixes: dict[int, str] | None = None,
    start_method: str = "spawn",
    numa_options: NumaOptions | None = None,
    duplicate_stdout_filters: list[str] | None = None,
    duplicate_stderr_filters: list[str] | None = None,
) -> PContext:
    """
    Start ``n`` copies of ``entrypoint`` processes with the provided options.

    ``entrypoint`` is either a ``Callable`` (function) or a ``str`` (binary).
    The number of copies is determined by the number of entries for ``args`` and
    ``envs`` arguments, which need to have the same key set.

    ``args`` and ``env`` parameters are the arguments and environment variables
    to pass down to the entrypoint mapped by the replica index (local rank).
    All local ranks must be accounted for.
    That is, the keyset should be ``{0,1,...,(nprocs-1)}``.

    .. note:: When the ``entrypoint`` is a binary (``str``), ``args`` can only be strings.
              If any other type is given, then it is casted to a string representation
              (e.g. ``str(arg1)``). Furthermore, a binary failure will only write
              an ``error.json`` error file if the main function is annotated with
              ``torch.distributed.elastic.multiprocessing.errors.record``. For function launches,
              this is done by default and there is no need to manually annotate
              with the ``@record`` annotation.

    Inside ``logs_specs``, ``redirects`` and ``tee`` are bitmasks specifying which std
    stream(s) to redirect to a log file in the ``log_dir``. Valid mask values are defined
    in ``Std``.  To redirect/tee only certain local ranks, pass ``redirects`` as a map
    with the key as the local rank to specify the redirect behavior for.
    Any missing local ranks will default to ``Std.NONE``.

    ``duplicate_stdout_filters`` and ``duplicate_stderr_filters``, if non-empty,
    duplicate stdouts and stderrs respectively specified in ``logs_specs``'s ``tee``
    to a file containing only lines that match _any_ of the filter strings. The log
    file is aggregated across all ranks selected by ``tee``.

    ``tee`` acts like the unix "tee" command in that it redirects + prints to console.
    To avoid worker stdout/stderr from printing to console, use the ``redirects`` parameter.

    For each process, the ``log_dir`` will contain:

    #. ``{local_rank}/error.json``: if the process failed, a file with the error info
    #. ``{local_rank}/stdout.log``: if ``redirect & STDOUT == STDOUT``
    #. ``{local_rank}/stderr.log``: if ``redirect & STDERR == STDERR``
    #. ``filtered_stdout.log``: if ``duplicate_stdout_filters`` is non-empty
    #. ``filtered_stderr.log``: if ``duplicate_stderr_filters`` is non-empty

    .. note:: It is expected that the ``log_dir`` exists, is empty, and is a directory.

    Example:
    ::

     log_dir = "/tmp/test"

     # ok; two copies of foo: foo("bar0"), foo("bar1")
     start_processes(
        name="trainer",
        entrypoint=foo,
        args:{0:("bar0",), 1:("bar1",),
        envs:{0:{}, 1:{}},
        log_dir=log_dir
     )

     # invalid; envs missing for local rank 1
     start_processes(
        name="trainer",
        entrypoint=foo,
        args:{0:("bar0",), 1:("bar1",),
        envs:{0:{}},
        log_dir=log_dir
     )

     # ok; two copies of /usr/bin/touch: touch file1, touch file2
     start_processes(
        name="trainer",
        entrypoint="/usr/bin/touch",
        args:{0:("file1",), 1:("file2",),
        envs:{0:{}, 1:{}},
        log_dir=log_dir
      )

     # caution; arguments casted to string, runs:
     # echo "1" "2" "3" and echo "[1, 2, 3]"
     start_processes(
        name="trainer",
        entrypoint="/usr/bin/echo",
        args:{0:(1,2,3), 1:([1,2,3],),
        envs:{0:{}, 1:{}},
        log_dir=log_dir
      )

    Args:
        name: a human readable short name that describes what the processes are
              (used as header when tee'ing stdout/stderr outputs)
        entrypoint: either a ``Callable`` (function) or ``cmd`` (binary)
        args: arguments to each replica
        envs: env vars to each replica
        log_dir: directory used to write log files
        start_method: multiprocessing start method (spawn, fork, forkserver)
                      ignored for binaries
        logs_specs: defines ``log_dir``, ``redirects``, and ``tee``.
                    inside ``logs_specs``:
                    - redirects: which std streams to redirect to a log file
                    - tee: which std streams to redirect + print to console
        local_ranks_filter: which ranks' logs to print to console
        duplicate_stdout_filters: filters for the duplicated stdout logs
        duplicate_stderr_filters: filters for the duplicated stderr logs

    """

    nprocs = len(args)
    _validate_full_rank(args, nprocs, "args")
    _validate_full_rank(envs, nprocs, "envs")

    context: PContext
    if isinstance(entrypoint, str):
        context = SubprocessContext(
            name=name,
            entrypoint=entrypoint,
            args=args,
            envs=envs,
            duplicate_stdout_filters=duplicate_stdout_filters,
            duplicate_stderr_filters=duplicate_stderr_filters,
            logs_specs=logs_specs,
            log_line_prefixes=log_line_prefixes,
            numa_options=numa_options,
        )
    else:
        context = MultiprocessContext(
            name=name,
            entrypoint=entrypoint,
            args=args,
            envs=envs,
            duplicate_stdout_filters=duplicate_stdout_filters,
            duplicate_stderr_filters=duplicate_stderr_filters,
            log_line_prefixes=log_line_prefixes,
            start_method=start_method,
            logs_specs=logs_specs,
            numa_options=numa_options,
        )

    try:
        context.start()
        return context
    except Exception:
        context.close()
        raise

