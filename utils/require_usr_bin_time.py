
def require_usr_bin_time(test_case):
    """
    Decorator marking a test that requires `/usr/bin/time`
    """
    return unittest.skipUnless(cmd_exists("/usr/bin/time"), "test requires /usr/bin/time")(test_case)

