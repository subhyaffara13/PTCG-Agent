
def xfailIfACL(func):
    return unittest.expectedFailure(func) if TEST_ACL else func

