
def raise_on_run_directly(file_to_call):
    raise RuntimeError("This test file is not meant to be run directly, "
                       f"use:\n\n\tpython {file_to_call} TESTNAME\n\n"
                       "instead.")

