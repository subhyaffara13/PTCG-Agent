
def test_editable_with_single_module(tmp_path, venv, editable_opts):
    files = {
        "mypkg": {
            "pyproject.toml": dedent(
                """\
                [build-system]
                requires = ["setuptools", "wheel"]
                build-backend = "setuptools.build_meta"

                [project]
                name = "mod"
                version = "3.14159"

                [tool.setuptools]
                py-modules = ["mod"]
                """
            ),
            "mod.py": "b = 2",
        },
    }
    jaraco.path.build(files, prefix=tmp_path)
    project = tmp_path / "mypkg"

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
    cmd = ["python", "-c", "import mod; print(mod.b)"]
    assert venv.run(cmd).strip() == "2"

