
def xfailIfDistributedNotSupported(func):
    return func if not (IS_MACOS or IS_JETSON) else unittest.expectedFailure(func)

