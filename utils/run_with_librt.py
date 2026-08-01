
def run_with_librt(
    file_path: str, experimental: bool = True, check: bool = True, opt_level: str = "0"
) -> subprocess.CompletedProcess[str]:
    """Run a Python file in a subprocess with built librt available.

    This runs the file in a fresh Python process where the built librt
    is at the front of sys.path, avoiding conflicts with any system librt.

    Args:
        file_path: Path to Python file to execute.
        experimental: Whether to use experimental features.
        check: If True, raise CalledProcessError on non-zero exit.
        opt_level: Optimization level ("0".."3") used when building librt.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.
    """
    librt_path = get_librt_path(experimental, opt_level=opt_level)
    # Prepend librt path to PYTHONPATH
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = librt_path + (os.pathsep + existing if existing else "")

    return subprocess.run(
        [sys.executable, file_path], capture_output=True, text=True, check=check, env=env
    )

