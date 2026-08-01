
def tests_build_wheel(monkeypatch, tmpdir):
    monkeypatch.chdir(MAIN_DIR)

    subprocess.run(
        [sys.executable, "-m", "pip", "wheel", ".", "-w", str(tmpdir)], check=True
    )

    (wheel,) = tmpdir.visit("*.whl")

    files = {f"pybind11/{n}" for n in all_files}
    files |= {
        "dist-info/LICENSE",
        "dist-info/METADATA",
        "dist-info/RECORD",
        "dist-info/WHEEL",
        "dist-info/entry_points.txt",
        "dist-info/top_level.txt",
    }

    with zipfile.ZipFile(str(wheel)) as z:
        names = z.namelist()

    trimmed = {n for n in names if "dist-info" not in n}
    trimmed |= {f"dist-info/{n.split('/', 1)[-1]}" for n in names if "dist-info" in n}
    assert files == trimmed

