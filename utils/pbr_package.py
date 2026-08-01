
def pbr_package(tmp_path, monkeypatch, venv):
    files = {
        "pyproject.toml": DALS(
            """
            [build-system]
            requires = ["setuptools"]
            build-backend = "setuptools.build_meta"
            """
        ),
        "setup.py": DALS(
            """
            __import__('setuptools').setup(
                pbr=True,
                setup_requires=["pbr"],
            )
            """
        ),
        "setup.cfg": DALS(
            """
            [metadata]
            name = mypkg

            [files]
            packages =
                mypkg
            """
        ),
        "mypkg": {
            "__init__.py": "",
            "hello.py": "print('Hello world!')",
        },
        "other": {"test.txt": "Another file in here."},
    }
    venv.run(["python", "-m", "pip", "install", "pbr"])
    prefix = tmp_path / 'mypkg'
    prefix.mkdir()
    jaraco.path.build(files, prefix=prefix)
    monkeypatch.setenv('PBR_VERSION', "0.42")
    return prefix

