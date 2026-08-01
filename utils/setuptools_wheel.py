
def setuptools_wheel(tmp_path_factory, request):
    prebuilt = os.getenv("PRE_BUILT_SETUPTOOLS_WHEEL")
    if prebuilt and os.path.exists(prebuilt):  # pragma: no cover
        return Path(prebuilt).resolve()

    _, wheel = _build_distributions(tmp_path_factory, request)
    return wheel

