import subprocess
import sys

def _python_executable_from_version(python_version: tuple[int, int]) -> str:
    if sys.version_info[:2] == python_version:
        return sys.executable
    str_ver = ".".join(map(str, python_version))
    try:
        sys_exe = (
            subprocess.check_output(
                python_executable_prefix(str_ver) + ["-c", "import sys; print(sys.executable)"],
                stderr=subprocess.STDOUT,
            )
            .decode()
            .strip()
        )
        return sys_exe
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise PythonExecutableInferenceError(
            "failed to find a Python executable matching version {},"
            " perhaps try --python-executable, or --no-site-packages?".format(python_version)
        ) from e

