import os

def test_gh21999_file_not_exist():
    tmpdir = mkdtemp(suffix=str(threading.get_native_id()))
    wrong_fn = os.path.join(tmpdir, 'not_exist_test_file.mtx')
    assert_raises(FileNotFoundError, mmread, wrong_fn)

