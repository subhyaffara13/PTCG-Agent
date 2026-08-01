
def check_sparse_version(min_ver):
    if sparse is None:
        return pytest.mark.skip(reason="sparse is not installed")
    return pytest.mark.skipif(
        version.parse(sparse.__version__) < version.Version(min_ver),
        reason=f"sparse version >= {min_ver} required"
    )

