
def test_lockfilefailure(tmp_path):
    # The logic here:
    # 1. get a temp directory from pytest
    # 2. import matplotlib which makes sure it exists
    # 3. get the cache dir (where we check it is writable)
    # 4. make it not writable
    # 5. try to write into it via font manager
    proc = subprocess_run_for_testing(
        [
            sys.executable,
            "-c",
            "import matplotlib;"
            "import os;"
            "p = matplotlib.get_cachedir();"
            "os.chmod(p, 0o555);"
            "import matplotlib.font_manager;"
        ],
        env={**os.environ, 'MPLCONFIGDIR': str(tmp_path)},
        check=True
    )

