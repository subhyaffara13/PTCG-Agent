
def test_iter_files_stdin(iter_files):
    assert iter_files(['-']) == ['-']

