import os
import sys

def read_types_packages_to_install(cache_dir: str, after_run: bool) -> list[str]:
    if not os.path.isdir(cache_dir):
        if not after_run:
            sys.stderr.write(
                "error: Can't determine which types to install with no files to check "
                "(and no cache from previous mypy run)\n"
            )
        else:
            sys.stderr.write(
                "error: --install-types failed (an error blocked analysis of which types to install)\n"
            )
    fnam = build.missing_stubs_file(cache_dir)
    if not os.path.isfile(fnam):
        # No missing stubs.
        return []
    with open(fnam) as f:
        return [line.strip() for line in f]

