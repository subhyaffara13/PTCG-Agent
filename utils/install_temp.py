import os
import subprocess
import sys

def install_temp(tmpdir_factory):
    # Based in part on test_cython from random.tests.test_extending
    if IS_WASM:
        pytest.skip("No subprocess")

    # Build against a copy of the sources placed next to the build dir:
    # meson refers to sources via paths relative to the build dir, and on
    # Windows the unnormalized cwd + `..` chain joining the deeply nested
    # pytest tmp dir and site-packages can exceed MAX_PATH, failing the
    # compile with "Cannot open source file".
    tmp_root = tmpdir_factory.mktemp("cython_test")
    srcdir = str(tmp_root / "src")
    shutil.copytree(
        os.path.join(os.path.dirname(__file__), 'examples', 'cython'),
        srcdir)
    build_dir = tmp_root / "build"
    os.makedirs(build_dir, exist_ok=True)
    # Ensure we use the correct Python interpreter even when `meson` is
    # installed in a different Python environment (see gh-24956)
    native_file = str(build_dir / 'interpreter-native-file.ini')
    with open(native_file, 'w') as f:
        f.write("[binaries]\n")
        f.write(f"python = '{sys.executable}'\n")
        f.write(f"python3 = '{sys.executable}'")

    try:
        subprocess.check_call(["meson", "--version"])
    except FileNotFoundError:
        pytest.skip("No usable 'meson' found")
    if sysconfig.get_platform() == "win-arm64":
        pytest.skip("Meson unable to find MSVC linker on win-arm64")
    if sys.platform == "win32":
        run_subprocess(["meson", "setup",
                        "--buildtype=release",
                        "--vsenv", "--native-file", native_file,
                        str(srcdir)],
                       build_dir)
    else:
        run_subprocess(["meson", "setup",
                        "--native-file", native_file, str(srcdir)],
                       build_dir)
    run_subprocess(["meson", "compile", "-vv"], build_dir)

    sys.path.append(str(build_dir))


def install_temp(tmpdir_factory):
    # Based in part on test_cython from random.tests.test_extending
    if IS_WASM:
        pytest.skip("No subprocess")

    # Build against a copy of the sources placed next to the build dir:
    # meson refers to sources via paths relative to the build dir, and on
    # Windows the unnormalized cwd + `..` chain joining the deeply nested
    # pytest tmp dir and site-packages can exceed MAX_PATH, failing the
    # compile with "Cannot open source file".
    tmp_root = tmpdir_factory.mktemp("limited_api")
    srcdir = str(tmp_root / "src")
    shutil.copytree(
        os.path.join(os.path.dirname(__file__), 'examples', 'limited_api'),
        srcdir)
    build_dir = tmp_root / "build"
    os.makedirs(build_dir, exist_ok=True)
    # Ensure we use the correct Python interpreter even when `meson` is
    # installed in a different Python environment (see gh-24956)
    native_file = str(build_dir / 'interpreter-native-file.ini')
    with open(native_file, 'w') as f:
        f.write("[binaries]\n")
        f.write(f"python = '{sys.executable}'\n")
        f.write(f"python3 = '{sys.executable}'")

    try:
        subprocess.check_call(["meson", "--version"])
    except FileNotFoundError:
        pytest.skip("No usable 'meson' found")
    if sysconfig.get_platform() == "win-arm64":
        pytest.skip("Meson unable to find MSVC linker on win-arm64")
    if sys.platform == "win32":
        run_subprocess(["meson", "setup",
                        "--werror",
                        "--buildtype=release",
                        "--vsenv", "--native-file", native_file,
                        str(srcdir)],
                       build_dir)
    else:
        run_subprocess(["meson", "setup", "--werror",
                        "--native-file", native_file, str(srcdir)],
                       build_dir)
    run_subprocess(["meson", "compile", "-vv"], build_dir)

    sys.path.append(str(build_dir))

