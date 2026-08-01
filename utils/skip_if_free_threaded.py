
def skipIfFreeThreaded(msg="Test doesn't work with free-threaded python"):
    if not isinstance(msg, str):
        raise AssertionError("Are you using skipIfFreeThreaded correctly?")
    return unittest.skipIf(sysconfig.get_config_var("Py_GIL_DISABLED") == 1, msg)

