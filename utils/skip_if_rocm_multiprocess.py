
def skip_if_rocm_multiprocess(func):
    """Skips a test for ROCm multiprocess UTs"""
    return unittest.skipIf(TEST_WITH_ROCM, TEST_SKIPS["skipIfRocm"].message)(func)

