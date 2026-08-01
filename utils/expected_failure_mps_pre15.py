
def expectedFailureMPSPre15(fn):
    import platform

    version = float(".".join(platform.mac_ver()[0].split(".")[:2]) or -1)
    if not version or version < 1.0:  # cpu or other unsupported device
        return fn
    if version < 15.0:
        return expectedFailure("mps")(fn)
    return fn

