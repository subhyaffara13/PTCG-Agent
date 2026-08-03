import sys

def use_multiprocessing_forkserver_on_linux():
    if sys.platform != "linux":
        # The default on Windows and macOS is "spawn": If it's not broken, don't fix it.
        return

    # Full background: https://github.com/pybind/pybind11/issues/4105#issuecomment-1301004592
    # In a nutshell: fork() after starting threads == flakiness in the form of deadlocks.
    # It is actually a well-known pitfall, unfortunately without guard rails.
    # "forkserver" is more performant than "spawn" (~9s vs ~13s for tests/test_gil_scoped.py,
    # visit the issuecomment link above for details).
    multiprocessing.set_start_method("forkserver")

