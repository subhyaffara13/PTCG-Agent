
def xfailIfSM12X(func):
    return func if not IS_SM12X else unittest.expectedFailure(func)

