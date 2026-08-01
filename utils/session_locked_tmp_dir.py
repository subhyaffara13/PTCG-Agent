
def session_locked_tmp_dir(request, tmp_path_factory, name):
    """Uses a file lock to guarantee only one worker can access a temp dir"""
    # get the temp directory shared by all workers
    base = tmp_path_factory.getbasetemp()
    shared_dir = base.parent if multiproc(request) else base

    locked_dir = shared_dir / name
    with FileLock(locked_dir.with_suffix(".lock")):
        # ^-- prevent multiple workers to access the directory at once
        locked_dir.mkdir(exist_ok=True, parents=True)
        yield locked_dir

