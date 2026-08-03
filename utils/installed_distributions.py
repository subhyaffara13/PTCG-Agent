import os
from typing import Dict, List

def installed_distributions(
    local: bool = False, paths: List[os.PathLike] = []
) -> Dict[str, Distribution]:
    # Check whether our version of pip supports the `--path` parameter
    if pip_api.PIP_VERSION < parse("19.2") and paths:
        raise PipError(
            f"pip {pip_api.PIP_VERSION} does not support the `paths` argument"
        )
    if pip_api.PIP_VERSION < parse("9.0.0"):
        return _old_installed_distributions(local)
    return _new_installed_distributions(local, paths)

