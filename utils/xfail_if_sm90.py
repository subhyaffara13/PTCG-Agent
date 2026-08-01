
def xfailIfSM90(func):
    return func if not IS_SM90 else unittest.expectedFailure(func)

