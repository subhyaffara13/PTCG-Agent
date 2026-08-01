
def test_savefig_rcparam(tmp_path):
    subprocess_run_helper(
        _test_savefig_rcparam, timeout=_test_timeout,
        extra_env={"MPLBACKEND": "macosx", "TEST_SAVEFIG_PATH": tmp_path})

