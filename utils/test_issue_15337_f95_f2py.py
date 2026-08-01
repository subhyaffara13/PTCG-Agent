
def test_issue_15337_f95_f2py():
    has_module('f2py')
    runtest_issue_15337('f95', 'f2py')

