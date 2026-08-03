import os
import subprocess
import sys

def install_package(
    pkg: str, python_executable: str = sys.executable, editable: bool = False
) -> None:
    """Install a package from test-data/packages/pkg/"""
    working_dir = os.path.join(package_path, pkg)
    with tempfile.TemporaryDirectory() as dir:
        install_cmd = [python_executable, "-m", "pip", "install"]
        if editable:
            install_cmd.append("-e")
        install_cmd.append(".")

        # Note that newer versions of pip (21.3+) don't
        # follow this env variable, but this is for compatibility
        env = {"PIP_BUILD": dir}
        # Inherit environment for Windows
        env.update(os.environ)
        try:
            with filelock.FileLock(pip_lock, timeout=pip_timeout):
                proc = subprocess.run(install_cmd, cwd=working_dir, capture_output=True, env=env)
        except filelock.Timeout as err:
            raise Exception(f"Failed to acquire {pip_lock}") from err
    if proc.returncode != 0:
        raise Exception(proc.stdout.decode("utf-8") + proc.stderr.decode("utf-8"))

