
def _cpu_count() -> int:
    """Use sched_affinity if available for virtualized or containerized
    environments.
    """
    cpu_share = _query_cpu()
    cpu_count = None
    sched_getaffinity = getattr(os, "sched_getaffinity", None)
    # pylint: disable=not-callable,using-constant-test,useless-suppression
    if sched_getaffinity:
        cpu_count = len(sched_getaffinity(0))
    elif multiprocessing:
        cpu_count = multiprocessing.cpu_count()
    else:
        cpu_count = 1
    if sys.platform == "win32":
        # See also https://github.com/python/cpython/issues/94242
        cpu_count = min(cpu_count, 56)  # pragma: no cover
    if cpu_share is not None:
        return min(cpu_share, cpu_count)
    return cpu_count


def _cpu_count():
    try:
        return mp.cpu_count()
    except NotImplementedError:  # pragma: no cover
        return 1

