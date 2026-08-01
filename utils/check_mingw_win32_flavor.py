
def check_mingw_win32_flavor(compiler: str) -> str:
    """
    Check if MinGW `compiler` exists and return it's flavor (win32 or posix).
    """
    try:
        out = subprocess.check_output(
            [compiler, "-v"], stderr=subprocess.STDOUT, text=True
        )
    except FileNotFoundError as e:
        raise RuntimeError(f"Compiler: {compiler} is not found.") from e
    except Exception as e:
        raise RuntimeError(f"Failed to run {compiler} -v") from e

    flavor: str | None = None
    for line in out.splitlines():
        if "Thread model" in line:
            flavor = line.split(":", 1)[-1].strip().lower()

    if flavor is None:
        raise RuntimeError(
            f"Cannot determine the flavor of {compiler} (win32 or posix). No Thread model found in {compiler} -v"
        )

    if flavor not in ("win32", "posix"):
        raise RuntimeError(
            f"Only win32 and pofix flavor of {compiler} is supported. The flavor is {flavor}"
        )

    return flavor

