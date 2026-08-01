
def tests_build_global_wheel(monkeypatch, tmpdir):
    monkeypatch.chdir(MAIN_DIR)
    monkeypatch.setenv("PYBIND11_GLOBAL_SDIST", "1")

    subprocess.run(
        [sys.executable, "-m", "pip", "wheel", ".", "-w", str(tmpdir)], check=True
    )

    (wheel,) = tmpdir.visit("*.whl")

    files = {f"data/data/{n}" for n in src_files}
    files |= {f"data/headers/{n[8:]}" for n in headers}
    files |= {
        "dist-info/LICENSE",
        "dist-info/METADATA",
        "dist-info/WHEEL",
        "dist-info/top_level.txt",
        "dist-info/RECORD",
    }

    with zipfile.ZipFile(str(wheel)) as z:
        names = z.namelist()

    beginning = names[0].split("/", 1)[0].rsplit(".", 1)[0]
    trimmed = {n[len(beginning) + 1 :] for n in names}

    assert files == trimmed

