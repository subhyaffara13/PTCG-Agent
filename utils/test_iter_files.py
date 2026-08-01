
def test_iter_files(mocker, iter_files):
    os_mod = mocker.patch('radon.cli.tools.os')
    os_path_mod = mocker.patch('radon.cli.tools.os.path')
    os_path_mod.normpath = os.path.normpath
    os_path_mod.basename = os.path.basename
    os_path_mod.join = os.path.join

    os_path_mod.isfile.side_effect = fake_isfile
    _orig_walk = os_mod.walk
    os_mod.walk = fake_walk
    _orig_is_python_file = tools._is_python_file
    tools._is_python_file = fake_is_python_file

    assert_pequal(
        iter_files(['file.py', 'random/path']),
        [
            'file.py',
            'amod.py',
            'test_all.py',
            'tests/test_amod.py',
            'tests/run.py',
            'sub/amod.py',
            'sub/bmod.py',
        ],
    )

    assert_pequal(
        iter_files(['file.py', 'random/path'], 'test_*'),
        [
            'file.py',
            'amod.py',
            'tests/test_amod.py',
            'tests/run.py',
            'sub/amod.py',
            'sub/bmod.py',
        ],
    )

    assert_pequal(
        iter_files(['file.py', 'random/path'], '*test_*'),
        ['file.py', 'amod.py', 'tests/run.py', 'sub/amod.py', 'sub/bmod.py'],
    )

    assert_pequal(
        iter_files(['file.py', 'random/path'], '*/test_*,amod*'),
        [
            'file.py',
            'test_all.py',
            'tests/run.py',
            'sub/amod.py',
            'sub/bmod.py',
        ],
    )

    assert_pequal(
        iter_files(['file.py', 'random/path'], None, 'tests'),
        ['file.py', 'amod.py', 'test_all.py', 'sub/amod.py', 'sub/bmod.py'],
    )

    assert_pequal(
        iter_files(['file.py', 'random/path'], None, 'tests,sub'),
        ['file.py', 'amod.py', 'test_all.py'],
    )
    tools._is_python_file = _orig_is_python_file
    os_mod.walk = _orig_walk

