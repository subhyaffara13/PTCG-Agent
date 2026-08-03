import os
from pathlib import Path


def _get_dist(dist_path, attrs):
    root = "/".join(os.path.split(dist_path))  # POSIX-style

    script = dist_path / 'setup.py'
    if script.exists():
        with Path(dist_path):
            dist = cast(
                Distribution,
                distutils.core.run_setup("setup.py", {}, stop_after="init"),
            )
    else:
        dist = Distribution(attrs)

    dist.src_root = root
    dist.script_name = "setup.py"
    with Path(dist_path):
        dist.parse_config_files()

    dist.set_defaults()
    return dist

