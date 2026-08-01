
def wait_all(futures: list[Future]) -> list:
    r"""
    Waits for all provided futures to be complete, and returns
    the list of completed values. If any of the futures encounters an error,
    the method will exit early and report the error not waiting for other
    futures to complete.

    Args:
        futures (list): a list of :class:`~torch.futures.Future` object.

    Returns:
        A list of the completed :class:`~torch.futures.Future` results. This
        method will throw an error if ``wait`` on any
        :class:`~torch.futures.Future` throws.
    """
    return [
        fut.wait()
        for fut in torch._C._collect_all(cast(list[torch._C.Future], futures)).wait()
    ]


def wait_all(work: Work | list[Work | None] | None) -> None:
    """
    Waits for all work objects in the input to complete.

    A single Work object, None, or a list of Work objects (possibly containing None).
    If None, does nothing. If a single Work, waits for it to complete. If a list, waits
    for each non-None Work in the list to complete.
    """

    if work is None:
        return
    if isinstance(work, Work):
        work = [work]
    for w in work:
        if w is None:
            continue
        w.wait()

