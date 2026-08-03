import os
from pathlib import Path


def run_subprocess(cmd, cwd=None, **kwargs):
    """Run ``cmd`` in a subprocess, failing the test with its captured output
    if it exits with a nonzero status.

    Output that a subprocess merely inherits is lost in pytest-xdist workers
    when a test fails, making CI failures hard to debug.  Routing a
    build/compile/run step through this helper captures the child's stdout and
    stderr and folds them into the failure message so they reach the report.
    Returns the ``subprocess.CompletedProcess`` for callers that want to
    inspect the output.  Extra keyword arguments are passed to
    ``subprocess.run``.
    """
    import subprocess

    import pytest

    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                         errors="replace", **kwargs)
    if res.returncode != 0:
        cmd_str = cmd if isinstance(cmd, str) else " ".join(map(str, cmd))
        in_dir = f" in {cwd}" if cwd is not None else ""
        pytest.fail(
            f"`{cmd_str}` failed (exit {res.returncode}){in_dir}\n"
            f"----- stdout -----\n{res.stdout}\n"
            f"----- stderr -----\n{res.stderr}",
            pytrace=False)
    return res


def run_subprocess(
    command: str | list[str],
    folder: str | Path | None = None,
    check=True,
    **kwargs,
) -> subprocess.CompletedProcess:
    """
    Method to run subprocesses. Calling this will capture the `stderr` and `stdout`,
    please call `subprocess.run` manually in case you would like for them not to
    be captured.

    Args:
        command (`str` or `list[str]`):
            The command to execute as a string or list of strings.
        folder (`str`, *optional*):
            The folder in which to run the command. Defaults to current working
            directory (from `os.getcwd()`).
        check (`bool`, *optional*, defaults to `True`):
            Setting `check` to `True` will raise a `subprocess.CalledProcessError`
            when the subprocess has a non-zero exit code.
        kwargs (`dict[str]`):
            Keyword arguments to be passed to the `subprocess.run` underlying command.

    Returns:
        `subprocess.CompletedProcess`: The completed process.
    """
    if isinstance(command, str):
        command = command.split()

    if isinstance(folder, Path):
        folder = str(folder)

    return subprocess.run(
        command,
        capture_output=True,
        check=check,
        encoding="utf-8",
        errors="replace",  # if not utf-8, replace char by �
        cwd=folder or os.getcwd(),
        **kwargs,
    )

