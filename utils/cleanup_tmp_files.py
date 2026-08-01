
def cleanup_tmp_files(test_func):
    """
    A decorator to help test codes remove temporary files after the tests.
    """
    def wrapper_function():
        try:
            test_func()
        finally:
            TmpFileManager.cleanup()

    return wrapper_function

