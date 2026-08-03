import subprocess

def _is_gnu_diff(diff_tool: str) -> bool:
    """Returns True if the provided diff executable is GNU diff."""
    try:
        proc = subprocess.run(
            [diff_tool, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:
        return False

    version_output = (proc.stdout or "") + (proc.stderr or "")
    return "GNU diffutils" in version_output

