import os
import subprocess
import sys

def get_librt_path(experimental: bool = True, opt_level: str = "0") -> str:
    """Get path to librt built from the repository, building and caching if necessary.

    Uses build/librt-cache/ under the repo root (gitignored). The cache is
    keyed by a hash of sources and build environment, so it auto-invalidates
    when relevant factors change.

    Safe to call from multiple parallel pytest workers - uses file locking.

    Args:
        experimental: Whether to enable experimental features.
        opt_level: Optimization level ("0".."3") used when building librt.

    Returns:
        Path to directory containing built librt modules.
    """
    # Use build/librt-cache/ under the repo root (gitignored)
    cache_root = os.path.join(PREFIX, "build", "librt-cache")
    build_hash = _librt_build_hash(experimental, opt_level)
    build_dir = os.path.join(cache_root, f"librt-{build_hash}")
    lock_file = os.path.join(cache_root, f"librt-{build_hash}.lock")
    marker = os.path.join(build_dir, ".complete")

    os.makedirs(cache_root, exist_ok=True)

    binary_suffix = ".pyd" if sys.platform == "win32" else ".so"

    with filelock.FileLock(lock_file, timeout=300):  # 5 min timeout
        # Reuse the cache only if the build completed *and* the compiled
        # binaries still exist. A repo-wide clean of .so/.pyd files can delete
        # the cached binaries while leaving the marker behind.
        if os.path.exists(marker) and any(
            f.endswith(binary_suffix) for f in os.listdir(os.path.join(build_dir, "librt"))
        ):
            return build_dir

        # Clean up any partial build
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        os.makedirs(build_dir)

        # Create librt package directory for --inplace to copy .so files into
        librt_pkg = os.path.join(build_dir, "librt")
        os.makedirs(librt_pkg)
        with open(os.path.join(librt_pkg, "__init__.py"), "w") as f:
            pass

        # Copy build_setup.py for per-file SIMD compiler flags
        build_setup_src = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build_setup.py"
        )
        build_setup_dst = os.path.join(build_dir, "build_setup.py")
        shutil.copy(build_setup_src, build_setup_dst)

        # Write setup.py
        setup_py = os.path.join(build_dir, "setup.py")
        with open(setup_py, "w") as f:
            f.write(_generate_setup_py(build_dir, experimental, opt_level))

        # Build (parallel builds don't work well because multiple extensions
        # share the same runtime C files, causing race conditions)
        result = subprocess.run(
            [sys.executable, setup_py, "build_ext", "--inplace"],
            cwd=build_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"librt build failed:\n{result.stdout}\n{result.stderr}")

        # Mark complete
        with open(marker, "w") as f:
            f.write("ok")

    return build_dir

