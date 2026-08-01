
def xfailIfLinux(func):
    return unittest.expectedFailure(func) if IS_LINUX and not TEST_WITH_ROCM and not IS_FBCODE else func

