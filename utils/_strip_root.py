
def _strip_root(x):
    if isinstance(x, str) and x.startswith("_export_root"):
        stripped = x[len("_export_root") :]
        return stripped.removeprefix(".")
    return x

