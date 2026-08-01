
def test_whos(version):
    for case in _cases(version):
        _whos_check_case(*case)

