import os
import sys

def _get_options_from_ini(ini_path, target):
    """Return a dictionary of config options or None if we can't load any."""
    ini_file = None

    if ini_path:
        ini_file = ini_path
    else:
        bandit_files = []

        for t in target:
            for root, _, filenames in os.walk(t):
                for filename in fnmatch.filter(filenames, ".bandit"):
                    bandit_files.append(os.path.join(root, filename))

        if len(bandit_files) > 1:
            LOG.error(
                "Multiple .bandit files found - scan separately or "
                "choose one with --ini\n\t%s",
                ", ".join(bandit_files),
            )
            sys.exit(2)

        elif len(bandit_files) == 1:
            ini_file = bandit_files[0]
            LOG.info("Found project level .bandit file: %s", bandit_files[0])

    if ini_file:
        return utils.parse_ini_file(ini_file)
    else:
        return None

