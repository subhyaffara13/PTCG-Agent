
def write_to_textfile(path: str, registry: Collector, escaping: str = openmetrics.ALLOWUTF8, tmpdir: Optional[str] = None) -> None:
    """Write metrics to the given path.

    This is intended for use with the Node exporter textfile collector.
    The path must end in .prom for the textfile collector to process it.

    An optional tmpdir parameter can be set to determine where the
    metrics will be temporarily written to. If not set, it will be in
    the same directory as the .prom file. If provided, the path MUST be
    on the same filesystem."""
    if tmpdir is not None:
        filename = os.path.basename(path)
        tmppath = f'{os.path.join(tmpdir, filename)}.{os.getpid()}.{threading.current_thread().ident}'
    else:
        tmppath = f'{path}.{os.getpid()}.{threading.current_thread().ident}'
    try:
        with open(tmppath, 'wb') as f:
            f.write(generate_latest(registry, escaping))

        # rename(2) is atomic but fails on Windows if the destination file exists
        if os.name == 'nt':
            os.replace(tmppath, path)
        else:
            os.rename(tmppath, path)
    except Exception:
        if os.path.exists(tmppath):
            os.remove(tmppath)
        raise

