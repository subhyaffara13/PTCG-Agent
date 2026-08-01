
def _load_json_file(
    file: str, manager: BuildManager, log_success: str, log_error: str
) -> dict[str, Any] | None:
    """A simple helper to read a JSON file with logging."""
    t0 = time.time()
    try:
        data = manager.metastore.read(file)
    except OSError:
        manager.log(log_error + file)
        return None
    manager.add_stats(metastore_read_time=time.time() - t0)
    # Only bother to compute the log message if we are logging it, since it could be big
    if manager.verbosity() >= 2:
        manager.trace(log_success + data.rstrip().decode())
    try:
        t1 = time.time()
        result = json_loads(data)
        manager.add_stats(data_file_load_time=time.time() - t1)
    except json.JSONDecodeError:
        manager.errors.set_file(file, None, manager.options)
        manager.error(
            None,
            "Error reading JSON file;"
            " you likely have a bad cache.\n"
            "Try removing the {cache_dir} directory"
            " and run mypy again.".format(cache_dir=manager.options.cache_dir),
            blocker=True,
        )
        return None
    else:
        assert isinstance(result, dict)
        return result


def _load_json_file(path):
    """Reads and loads JSON from the given path. Used to read both X509 workload certificate and
    secure connect configurations.

    Args:
        path (str): the path to read from.

    Returns:
        Dict[str, str]: The JSON stored at the file.

    Raises:
        google.auth.exceptions.ClientCertError: If failed to parse the file as JSON.
    """
    try:
        with open(path) as f:
            json_data = json.load(f)
    except ValueError as caught_exc:
        new_exc = exceptions.ClientCertError(caught_exc)
        raise new_exc from caught_exc

    return json_data

