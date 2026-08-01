
def xfailIfSM120OrLater(func):
    return func if not SM120OrLater else unittest.expectedFailure(func)

