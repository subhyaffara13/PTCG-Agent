import os
import sys

def get_pip_packages(run_lambda, patterns=None):
    """Return `pip list` output. Note: will also find conda-installed pytorch and numpy packages."""
    if patterns is None:
        patterns = PIP_PATTERNS + COMMON_PATTERNS + NVIDIA_PATTERNS + ONEAPI_PATTERNS

    pip_version = "pip3" if sys.version_info.major == 3 else "pip"

    os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    # People generally have pip as `pip` or `pip3`
    # But here it is invoked as `python -mpip`
    out = run_and_read_all(
        run_lambda, [sys.executable, "-mpip", "list", "--format=freeze"]
    )
    if out is None:
        return pip_version, out

    filtered_out = "\n".join(
        line for line in out.splitlines() if any(name in line for name in patterns)
    )

    return pip_version, filtered_out

