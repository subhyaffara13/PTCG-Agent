
def test_compat_install(tmp_path, venv):
    # TODO: Remove `compat` after Dec/2022.
    opts = ["--config-settings", "editable-mode=compat"]
    files = TestOverallBehaviour.EXAMPLES["custom-layout"]
    install_project("mypkg", venv, tmp_path, files, *opts)

    out = venv.run(["python", "-c", "import mypkg.mod1; print(mypkg.mod1.var)"])
    assert "42" in out

    expected_path = comparable_path(str(tmp_path))

    # Compatible behaviour will make spurious modules and excluded
    # files importable directly from the original path
    for cmd in (
        "import otherfile; print(otherfile)",
        "import other; print(other)",
        "import mypkg; print(mypkg)",
    ):
        out = comparable_path(venv.run(["python", "-c", cmd]))
        assert expected_path in out

    # Compatible behaviour will not consider custom mappings
    cmd = """\
    try:
        from mypkg import subpackage;
    except ImportError as ex:
        print(ex)
    """
    out = venv.run(["python", "-c", dedent(cmd)])
    assert "cannot import name 'subpackage'" in out

