import os
import sys

def python_subprocess_env() -> dict[str, str]:
    """
    Get a base environment for running Python subprocesses.
    """

    env = {
        # Inherit the environment of the current process.
        **os.environ,
        # Set the PYTHONPATH so the subprocess can find torch.
        "PYTHONPATH": os.environ.get(
            "TORCH_CUSTOM_PYTHONPATH", os.pathsep.join(sys.path)
        ),
    }

    # Set PYTHONHOME for internal builds, to account for builds that bundle the
    # runtime.  Otherwise they will use the libraries and headers from the
    # platform runtime instead.
    #
    # This can't be done for external builds.  The process can be run from a
    # venv and that won't include Python headers.  The process needs to be able
    # to search for and find the platform runtime.
    if config.is_fbcode():
        env["PYTHONHOME"] = sysconfig.get_path("data")

    return env

