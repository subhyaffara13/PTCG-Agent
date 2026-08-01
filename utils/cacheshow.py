
def cacheshow(config: Config, session: Session) -> int:
    """Display cache contents when --cache-show is used.

    Shows cached values and directories matching the specified glob pattern
    (default: '*'). Displays cache location, cached test results, and
    any cached directories created by plugins.

    :param config: pytest configuration object.
    :param session: pytest session object.
    :returns: Exit code (0 for success).
    """
    from pprint import pformat

    assert config.cache is not None

    tw = TerminalWriter()
    tw.line("cachedir: " + str(config.cache._cachedir))
    if not config.cache._cachedir.is_dir():
        tw.line("cache is empty")
        return 0

    glob = config.option.cacheshow[0]
    if glob is None:
        glob = "*"

    dummy = object()
    basedir = config.cache._cachedir
    vdir = basedir / Cache._CACHE_PREFIX_VALUES
    tw.sep("-", f"cache values for {glob!r}")
    for valpath in sorted(x for x in vdir.rglob(glob) if x.is_file()):
        key = str(valpath.relative_to(vdir))
        val = config.cache.get(key, dummy)
        if val is dummy:
            tw.line(f"{key} contains unreadable content, will be ignored")
        else:
            tw.line(f"{key} contains:")
            for line in pformat(val).splitlines():
                tw.line("  " + line)

    ddir = basedir / Cache._CACHE_PREFIX_DIRS
    if ddir.is_dir():
        contents = sorted(ddir.rglob(glob))
        tw.sep("-", f"cache directories for {glob!r}")
        for p in contents:
            # if p.is_dir():
            #    print("%s/" % p.relative_to(basedir))
            if p.is_file():
                key = str(p.relative_to(basedir))
                tw.line(f"{key} is a file of length {p.stat().st_size}")
    return 0

