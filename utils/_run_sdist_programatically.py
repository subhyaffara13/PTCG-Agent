from pathlib import Path


def _run_sdist_programatically(dist_path, attrs):
    dist = _get_dist(dist_path, attrs)
    cmd = sdist(dist)
    cmd.ensure_finalized()
    assert cmd.distribution.packages or cmd.distribution.py_modules

    with quiet(), Path(dist_path):
        cmd.run()

    return dist, cmd

