
def pytest_unconfigure() -> None:
    global RUNNER_CLASS

    RUNNER_CLASS = None


def pytest_unconfigure(config: Config) -> None:
    import faulthandler

    faulthandler.disable()
    # Close the dup file installed during pytest_configure.
    if fault_handler_stderr_fd_key in config.stash:
        os.close(config.stash[fault_handler_stderr_fd_key])
        del config.stash[fault_handler_stderr_fd_key]
    # Re-enable the faulthandler if it was originally enabled.
    if fault_handler_original_stderr_fd_key in config.stash:
        faulthandler.enable(config.stash[fault_handler_original_stderr_fd_key])
        del config.stash[fault_handler_original_stderr_fd_key]


def pytest_unconfigure(config: Config) -> None:
    """Called before test process is exited.

    :param config: The pytest config object.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """


def pytest_unconfigure(config: Config) -> None:
    xml = config.stash.get(xml_key, None)
    if xml:
        del config.stash[xml_key]
        config.pluginmanager.unregister(xml)


def pytest_unconfigure(config: Config) -> None:
    if pastebinfile_key in config.stash:
        pastebinfile = config.stash[pastebinfile_key]
        # Get terminal contents and delete file.
        pastebinfile.seek(0)
        sessionlog = pastebinfile.read()
        pastebinfile.close()
        del config.stash[pastebinfile_key]
        # Undo our patching in the terminal reporter.
        tr = config.pluginmanager.getplugin("terminalreporter")
        del tr._tw.__dict__["write"]
        # Write summary.
        tr.write_sep("=", "Sending information to Paste Service")
        pastebinurl = create_new_paste(sessionlog)
        tr.write_line(f"pastebin session-log: {pastebinurl}\n")


def pytest_unconfigure(config: Config) -> None:
    # Runs before ``_cleanup_stack.close()``, so warning filters from
    # cleanup-stack-managed contexts (notably the ``warnings`` plugin's
    # ``catch_warnings``) are still installed when garbage-collected
    # finalizers fire. A ``config.add_cleanup`` callback would instead
    # couple correctness to LIFO pop order across plugins' cleanups.
    if unraisable_exceptions not in config.stash:
        # ``pytest_configure`` did not complete (e.g. a usage error raised
        # in another plugin's configure), so the queue stash was never set.
        return
    # PyPy can resurrect objects in __del__, so it needs several GC passes
    # (5, per the Trio project); CPython frees cycles in one pass. See #14441.
    _default_gc_collect_iterations = 5 if sys.implementation.name == "pypy" else 1
    gc_collect_iterations = config.stash.get(
        gc_collect_iterations_key, _default_gc_collect_iterations
    )
    gc_collect_harder(gc_collect_iterations)
    collect_unraisable(config)


def pytest_unconfigure(config: Config) -> None:
    MARK_GEN._config = config.stash.get(old_mark_config_key, None)


def pytest_unconfigure(config):
    matplotlib._called_from_pytest = False

