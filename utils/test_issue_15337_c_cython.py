
def test_issue_15337_C_cython():
    has_module('Cython')
    runtest_issue_15337('C89', 'cython')

