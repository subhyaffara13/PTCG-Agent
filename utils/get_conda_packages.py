import os

def get_conda_packages(run_lambda, patterns=None):
    if patterns is None:
        patterns = CONDA_PATTERNS + COMMON_PATTERNS + NVIDIA_PATTERNS + ONEAPI_PATTERNS
    conda = os.environ.get("CONDA_EXE", "conda")
    out = run_and_read_all(run_lambda, "{} list".format(conda))
    if out is None:
        return out

    return "\n".join(
        line
        for line in out.splitlines()
        if not line.startswith("#") and any(name in line for name in patterns)
    )

