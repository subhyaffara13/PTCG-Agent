import os

def test_data_dir_with_tag_build(monkeypatch, tmp_path):
    """
    Setuptools allow authors to set PEP 440's local version segments
    using ``egg_info.tag_build``. This should be reflected not only in the
    ``.whl`` file name, but also in the ``.dist-info`` and ``.data`` dirs.
    See pypa/setuptools#3997.
    """
    monkeypatch.chdir(tmp_path)
    files = {
        "setup.py": """
            from setuptools import setup
            setup(headers=["hello.h"])
            """,
        "setup.cfg": """
            [metadata]
            name = test
            version = 1.0

            [options.data_files]
            hello/world = file.txt

            [egg_info]
            tag_build = +what
            tag_date = 0
            """,
        "file.txt": "",
        "hello.h": "",
    }
    for file, content in files.items():
        with open(file, "w", encoding="utf-8") as fh:
            fh.write(cleandoc(content))

    bdist_wheel_cmd().run()

    # Ensure .whl, .dist-info and .data contain the local segment
    wheel_path = "dist/test-1.0+what-py3-none-any.whl"
    assert os.path.exists(wheel_path)
    entries = set(ZipFile(wheel_path).namelist())
    for expected in (
        "test-1.0+what.data/headers/hello.h",
        "test-1.0+what.data/data/hello/world/file.txt",
        "test-1.0+what.dist-info/METADATA",
        "test-1.0+what.dist-info/WHEEL",
    ):
        assert expected in entries

    for not_expected in (
        "test.data/headers/hello.h",
        "test-1.0.data/data/hello/world/file.txt",
        "test.dist-info/METADATA",
        "test-1.0.dist-info/WHEEL",
    ):
        assert not_expected not in entries

