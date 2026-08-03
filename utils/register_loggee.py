import sys

def registerLoggee(module, name='LOG', flags=DEBUG_NONE):
    LOGGEE_MAP[sys.modules[module]] = name, flags
    setLogger(_LOG)
    return _LOG

