
def _find_vcvarsall(plat_spec):
    # bpo-38597: Removed vcruntime return value
    _, best_dir = _find_vc2017()

    if not best_dir:
        best_version, best_dir = _find_vc2015()

    if not best_dir:
        log.debug("No suitable Visual C++ version found")
        return None, None

    vcvarsall = os.path.join(best_dir, "vcvarsall.bat")
    if not os.path.isfile(vcvarsall):
        log.debug("%s cannot be found", vcvarsall)
        return None, None

    return vcvarsall, None

