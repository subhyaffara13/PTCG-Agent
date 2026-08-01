
def test_build_global_dist(monkeypatch, tmpdir):
    monkeypatch.chdir(MAIN_DIR)
    monkeypatch.setenv("PYBIND11_GLOBAL_SDIST", "1")
    subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--outdir", str(tmpdir)], check=True
    )

    (sdist,) = tmpdir.visit("*.tar.gz")

    with tarfile.open(str(sdist), "r:gz") as tar:
        start = tar.getnames()[0] + "/"
        version = start[16:-1]
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
    files |= {f"pybind11_global{n}" for n in local_sdist_files}
    assert simpler == files

    with open(os.path.join(MAIN_DIR, "tools", "setup_global.py.in"), "rb") as f:
        contents = (
            string.Template(f.read().decode())
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

