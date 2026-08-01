
def getsitepackages() -> list[str]:
    res = []
    if hasattr(site, "getsitepackages"):
        res.extend(site.getsitepackages())

        if hasattr(site, "getusersitepackages") and site.ENABLE_USER_SITE:
            res.insert(0, site.getusersitepackages())
    else:
        res = [sysconfig.get_paths()["purelib"]]
    return res

