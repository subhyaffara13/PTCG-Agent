
def _as_unc_path(host, path):
    rpath = path.replace("/", "\\")
    unc = f"\\\\{host}{rpath}"
    return unc

