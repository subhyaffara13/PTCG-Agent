import os
import subprocess
import sys

def test_build_sdist(monkeypatch, tmpdir):
    monkeypatch.chdir(MAIN_DIR)

    subprocess.run(
        [sys.executable, "-m", "build", "--sdist", f"--outdir={tmpdir}"], check=True
    )

    (sdist,) = tmpdir.visit("*.tar.gz")

    with tarfile.open(str(sdist), "r:gz") as tar:
        start = tar.getnames()[0] + "/"
        version = start[9:-1]
        simpler = {n.split("/", 1)[-1] for n in tar.getnames()[1:]}

        setup_py = read_tz_file(tar, "setup.py")
        pyproject_toml = read_tz_file(tar, "pyproject.toml")
        pkgconfig = read_tz_file(tar, "pybind11/share/pkgconfig/pybind11.pc")
        cmake_cfg = read_tz_file(
            tar, "pybind11/share/cmake/pybind11/pybind11Config.cmake"
        )

    assert (
        'set(pybind11_INCLUDE_DIR "${PACKAGE_PREFIX_DIR}/include")'
        in cmake_cfg.decode("utf-8")
    )

    files = {f"pybind11/{n}" for n in all_files}
    files |= sdist_files
    files |= {f"pybind11{n}" for n in local_sdist_files}
    files.add("pybind11.egg-info/entry_points.txt")
    files.add("pybind11.egg-info/requires.txt")
    assert simpler == files

    with open(os.path.join(MAIN_DIR, "tools", "setup_main.py.in"), "rb") as f:
        contents = (
            string.Template(f.read().decode("utf-8"))
            .substitute(version=version, extra_cmd="")
            .encode("utf-8")
        )
    assert setup_py == contents

    with open(os.path.join(MAIN_DIR, "tools", "pyproject.toml"), "rb") as f:
        contents = f.read()
    assert pyproject_toml == contents

    simple_version = ".".join(version.split(".")[:3])
    pkgconfig_expected = PKGCONFIG.format(VERSION=simple_version).encode("utf-8")
    assert normalize_line_endings(pkgconfig) == pkgconfig_expected

