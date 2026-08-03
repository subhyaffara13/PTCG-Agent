from pathlib import Path


def tmp_path(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Generator[Path]:
    """Return a temporary directory (as :class:`pathlib.Path` object)
    which is unique to each test function invocation.
    The temporary directory is created as a subdirectory
    of the base temporary directory, with configurable retention,
    as discussed in :ref:`temporary directory location and retention`.
    """
    path = _mk_tmp(request, tmp_path_factory)
    yield path

    # Remove the tmpdir if the policy is "failed" and the test passed.
    policy = tmp_path_factory._retention_policy
    result_dict = request.node.stash[tmppath_result_key]

    if policy == "failed" and result_dict.get("call", True):
        # We do a "best effort" to remove files, but it might not be possible due to some leaked resource,
        # permissions, etc, in which case we ignore it.
        rmtree(path, ignore_errors=True)

    del request.node.stash[tmppath_result_key]

