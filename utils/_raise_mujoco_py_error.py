from typing import Any

def _raise_mujoco_py_error(*args: Any, **kwargs: Any):
    raise ImportError(
        "The mujoco v2 and v3 based environments have been moved to the gymnasium-robotics project (https://github.com/Farama-Foundation/gymnasium-robotics)."
    )

