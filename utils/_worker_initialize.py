
def _worker_initialize(
    linter: bytes, extra_packages_paths: Sequence[str] | None = None
) -> None:
    """Function called to initialize a worker for a Process within a concurrent Pool.

    :param linter: A linter-class (PyLinter) instance pickled with dill
    :param extra_packages_paths: Extra entries to be added to `sys.path`
    """
    global _worker_linter  # pylint: disable=global-statement
    _worker_linter = dill.loads(linter)
    assert _worker_linter

    # On the worker process side the messages are just collected and passed back to
    # parent process as _worker_check_file function's return value
    _worker_linter.set_reporter(reporters.CollectingReporter())
    _worker_linter.open()

    # Re-register dynamic plugins, since the pool does not have access to the
    # astroid module that existed when the linter was pickled.
    _worker_linter.load_plugin_modules(_worker_linter._dynamic_plugins, force=True)
    _worker_linter.load_plugin_configuration()

    if extra_packages_paths:
        _augment_sys_path(extra_packages_paths)

