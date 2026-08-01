
def xfailIfSM100OrLater(func):
    return func if not SM100OrLater else unittest.expectedFailure(func)

