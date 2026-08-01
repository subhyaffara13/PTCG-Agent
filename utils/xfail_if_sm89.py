
def xfailIfSM89(func):
    return func if not IS_SM89 else unittest.expectedFailure(func)

