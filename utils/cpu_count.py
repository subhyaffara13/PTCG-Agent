import os

def cpu_count(logical=True):
    """Return the number of logical CPUs in the system (same as
    os.cpu_count()).

    If *logical* is False return the number of physical cores only
    (e.g. hyper thread CPUs are excluded).

    Return None if undetermined.

    The return value is cached after first call.
    If desired cache can be cleared like this:

    >>> psutil.cpu_count.cache_clear()
    """
    if logical:
        ret = _psplatform.cpu_count_logical()
    else:
        ret = _psplatform.cpu_count_cores()
    if ret is not None and ret < 1:
        ret = None
    return ret


def cpu_count() -> int | None:
    """Return the number of CPUs available to the current process.

    Prefers ``os.sched_getaffinity`` (respects cgroups / taskset) and
    falls back to ``os.cpu_count``.
    """
    # os.process_cpu_count was added in CPython 3.13, see
    # https://docs.python.org/3/library/os.html#os.process_cpu_count
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count()

