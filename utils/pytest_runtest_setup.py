
def pytest_runtest_setup(item):
    mark = item.get_closest_marker("xslow")
    if mark is not None:
        try:
            v = int(os.environ.get('SCIPY_XSLOW', '0'))
        except ValueError:
            v = False
        if not v:
            pytest.skip("very slow test; "
                        "set environment variable SCIPY_XSLOW=1 to run it")
    mark = item.get_closest_marker("xfail_on_32bit")
    if mark is not None and np.intp(0).itemsize < 8:
        pytest.xfail(f'Fails on our 32-bit test platform(s): {mark.args[0]}')

    # Older versions of threadpoolctl have an issue that may lead to this
    # warning being emitted, see gh-14441
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pytest.PytestUnraisableExceptionWarning)

        try:
            from threadpoolctl import threadpool_limits

            HAS_THREADPOOLCTL = True
        except Exception:  # observed in gh-14441: (ImportError, AttributeError)
            # Optional dependency only. All exceptions are caught, for robustness
            HAS_THREADPOOLCTL = False

        if HAS_THREADPOOLCTL:
            # Set the number of openmp threads based on the number of workers
            # xdist is using to prevent oversubscription. Simplified version of what
            # sklearn does (it can rely on threadpoolctl and its builtin OpenMP helper
            # functions)
            try:
                xdist_worker_count = int(os.environ['PYTEST_XDIST_WORKER_COUNT'])
            except KeyError:
                # raises when pytest-xdist is not installed
                return

            if not os.getenv('OMP_NUM_THREADS'):
                max_openmp_threads = os.cpu_count() // 2  # use nr of physical cores
                threads_per_worker = max(max_openmp_threads // xdist_worker_count, 1)
                try:
                    threadpool_limits(threads_per_worker, user_api='blas')
                except Exception:
                    # May raise AttributeError for older versions of OpenBLAS.
                    # Catch any error for robustness.
                    return


def pytest_runtest_setup(item: Item) -> None:
    """Called to perform the setup phase for a test item.

    The default implementation runs ``setup()`` on ``item`` and all of its
    parents (which haven't been setup yet). This includes obtaining the
    values of fixtures required by the item (which haven't been obtained
    yet).

    :param item:
        The item.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only conftest
    files in the item's directory and its parent directories are consulted.
    """


def pytest_runtest_setup(item: Item) -> None:
    _update_current_test_var(item, "setup")
    item.session._setupstate.setup(item)


def pytest_runtest_setup(item: Item) -> None:
    skipped = evaluate_skip_marks(item)
    if skipped:
        raise skip.Exception(skipped.reason, _use_item_location=True)

    item.stash[xfailed_key] = xfailed = evaluate_xfail_marks(item)
    if xfailed and not item.config.option.runxfail and not xfailed.run:
        xfail("[NOTRUN] " + xfailed.reason)


def pytest_runtest_setup(item: Item) -> None:
    collect_thread_exception(item.config)


def pytest_runtest_setup(item: Item) -> None:
    collect_unraisable(item.config)

