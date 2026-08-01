
def test_issue_10274_C_cython():
    has_module('Cython')
    runtest_issue_10274('C89', 'cython')

