import os
import subprocess
import sys

def _test_cython_extension(tmp_path, srcdir):
    """
    Helper function to test building and importing Cython modules that
    make use of the Cython APIs for BLAS, LAPACK, optimize, and special.
    """
    import pytest
    try:
        subprocess.check_call(["meson", "--version"])
    except FileNotFoundError:
        pytest.skip("No usable 'meson' found")

    # Make safe for being called by multiple threads within one test
    tmp_path = tmp_path / str(threading.get_ident())

    # build the examples in a temporary directory
    mod_name = os.path.split(srcdir)[1]
    shutil.copytree(srcdir, tmp_path / mod_name)
    build_dir = tmp_path / mod_name / 'tests' / '_cython_examples'
    target_dir = build_dir / 'build'
    os.makedirs(target_dir, exist_ok=True)

    # Ensure we use the correct Python interpreter even when `meson` is
    # installed in a different Python environment (see numpy#24956)
    native_file = str(build_dir / 'interpreter-native-file.ini')
    with open(native_file, 'w') as f:
        f.write("[binaries]\n")
        f.write(f"python = '{sys.executable}'")

    if sys.platform == "win32":
        subprocess.check_call(["meson", "setup",
                               "--buildtype=release",
                               "--native-file", native_file,
                               "--vsenv", str(build_dir)],
                              cwd=target_dir,
                              )
    else:
        subprocess.check_call(["meson", "setup",
                               "--native-file", native_file, str(build_dir)],
                              cwd=target_dir
                              )
    subprocess.check_call(["meson", "compile", "-vv"], cwd=target_dir)

    # import without adding the directory to sys.path
    suffix = sysconfig.get_config_var('EXT_SUFFIX')

    def load(modname):
        so = (target_dir / modname).with_suffix(suffix)
        spec = spec_from_file_location(modname, so)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    # test that the module can be imported
    return load("extending"), load("extending_cpp")

