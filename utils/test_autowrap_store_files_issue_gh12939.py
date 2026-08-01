
def test_autowrap_store_files_issue_gh12939():
    x, y = symbols('x y')
    tmp = './tmp'
    saved_cwd = os.getcwd()
    temp_cwd = tempfile.mkdtemp()
    try:
        os.chdir(temp_cwd)
        f = autowrap(x + y, backend='dummy', tempdir=tmp)
        assert f() == str(x + y)
        assert os.access(tmp, os.F_OK)
    finally:
        os.chdir(saved_cwd)
        shutil.rmtree(temp_cwd)

