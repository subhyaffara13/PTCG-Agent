
def setuptools_sdist(tmp_path_factory, request):
    prebuilt = os.getenv("PRE_BUILT_SETUPTOOLS_SDIST")
    if prebuilt and os.path.exists(prebuilt):  # pragma: no cover
        return Path(prebuilt).resolve()

    sdist, _ = _build_distributions(tmp_path_factory, request)
    return sdist

