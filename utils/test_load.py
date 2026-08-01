
def test_load(version):
    for case in _cases(version):
        _load_check_case(*case[:3])

