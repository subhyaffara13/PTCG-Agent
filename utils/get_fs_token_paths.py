
def get_fs_token_paths(
    urlpath,
    mode="rb",
    num=1,
    name_function=None,
    storage_options=None,
    protocol=None,
    expand=True,
):
    """Filesystem, deterministic token, and paths from a urlpath and options.

    Parameters
    ----------
    urlpath: string or iterable
        Absolute or relative filepath, URL (may include protocols like
        ``s3://``), or globstring pointing to data.
    mode: str, optional
        Mode in which to open files.
    num: int, optional
        If opening in writing mode, number of files we expect to create.
    name_function: callable, optional
        If opening in writing mode, this callable is used to generate path
        names. Names are generated for each partition by
        ``urlpath.replace('*', name_function(partition_index))``.
    storage_options: dict, optional
        Additional keywords to pass to the filesystem class.
    protocol: str or None
        To override the protocol specifier in the URL
    expand: bool
        Expand string paths for writing, assuming the path is a directory
    """
    if isinstance(urlpath, (list, tuple, set)):
        if not urlpath:
            raise ValueError("empty urlpath sequence")
        urlpath0 = stringify_path(next(iter(urlpath)))
    else:
        urlpath0 = stringify_path(urlpath)
    storage_options = storage_options or {}
    if protocol:
        storage_options["protocol"] = protocol
    chain = _un_chain(urlpath0, storage_options or {})
    inkwargs = {}
    # Reverse iterate the chain, creating a nested target_* structure
    for i, ch in enumerate(reversed(chain)):
        urls, nested_protocol, kw = ch
        if i == len(chain) - 1:
            inkwargs = dict(**kw, **inkwargs)
            continue
        inkwargs["target_options"] = dict(**kw, **inkwargs)
        inkwargs["target_protocol"] = nested_protocol
        inkwargs["fo"] = urls
    paths, protocol, _ = chain[0]
    fs = filesystem(protocol, **inkwargs)
    if isinstance(urlpath, (list, tuple, set)):
        pchains = [
            _un_chain(stringify_path(u), storage_options or {})[0] for u in urlpath
        ]
        if len({pc[1] for pc in pchains}) > 1:
            raise ValueError("Protocol mismatch getting fs from %s", urlpath)
        paths = [pc[0] for pc in pchains]
    else:
        paths = fs._strip_protocol(paths)
    if isinstance(paths, (list, tuple, set)):
        if expand:
            paths = expand_paths_if_needed(paths, mode, num, fs, name_function)
        elif not isinstance(paths, list):
            paths = list(paths)
    else:
        if ("w" in mode or "x" in mode) and expand:
            paths = _expand_paths(paths, name_function, num)
        elif "*" in paths:
            paths = [f for f in sorted(fs.glob(paths)) if not fs.isdir(f)]
        else:
            paths = [paths]

    return fs, fs._fs_token, paths

