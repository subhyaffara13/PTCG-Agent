
def setLogger(userLogger):
    global _LOG

    if userLogger:
        _LOG = userLogger
    else:
        _LOG = DEBUG_NONE

    # Update registered logging clients
    for module, (name, flags) in LOGGEE_MAP.items():
        setattr(module, name, _LOG & flags and _LOG or DEBUG_NONE)

