
def test_editable_with_pyproject(tmp_path, venv, files, editable_opts):
    project = tmp_path / "mypkg"
    project.mkdir()
    jaraco.path.build(files, prefix=project)

    cmd = [
        "python",
        "-m",
        "pip",
        "install",
        "--no-build-isolation",  # required to force current version of setuptools
        "-e",
        str(project),
        *editable_opts,
    ]
    print(venv.run(cmd))

    cmd = ["python", "-m", "mypkg"]
    assert venv.run(cmd).strip() == "3.14159.post0 Hello World"

    (project / "src/mypkg/data.txt").write_text("foobar", encoding="utf-8")
    (project / "src/mypkg/mod.py").write_text("x = 42", encoding="utf-8")
    assert venv.run(cmd).strip() == "3.14159.post0 foobar 42"

