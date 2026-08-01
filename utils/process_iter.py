
def process_iter(attrs=None, ad_value=None):
    """Return a generator yielding a Process instance for all
    running processes.

    Every new Process instance is only created once and then cached
    into an internal table which is updated every time this is used.
    Cache can optionally be cleared via `process_iter.cache_clear()`.

    The sorting order in which processes are yielded is based on
    their PIDs.

    *attrs* and *ad_value* have the same meaning as in
    Process.as_dict(). If *attrs* is specified as_dict() is called
    and the resulting dict is stored as a 'info' attribute attached
    to returned Process instance.
    If *attrs* is an empty list it will retrieve all process info
    (slow).
    """
    global _pmap

    def add(pid):
        proc = Process(pid)
        pmap[proc.pid] = proc
        return proc

    def remove(pid):
        pmap.pop(pid, None)

    pmap = _pmap.copy()
    a = set(pids())
    b = set(pmap.keys())
    new_pids = a - b
    gone_pids = b - a
    for pid in gone_pids:
        remove(pid)
    while _pids_reused:
        pid = _pids_reused.pop()
        debug(f"refreshing Process instance for reused PID {pid}")
        remove(pid)
    try:
        ls = sorted(list(pmap.items()) + list(dict.fromkeys(new_pids).items()))
        for pid, proc in ls:
            try:
                if proc is None:  # new process
                    proc = add(pid)
                if attrs is not None:
                    proc.info = proc.as_dict(attrs=attrs, ad_value=ad_value)
                yield proc
            except NoSuchProcess:
                remove(pid)
    finally:
        _pmap = pmap

