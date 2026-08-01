
def test_info_compute_numba():
    # GH#51922
    numba = pytest.importorskip("numba")
    if Version(numba.__version__) == Version("0.61") and is_platform_arm():
        pytest.skip(f"Segfaults on ARM platforms with numba {numba.__version__}")
    df = DataFrame([[1, 2], [3, 4]])

    with option_context("compute.use_numba", True):
        buf = StringIO()
        df.info(buf=buf)
        result = buf.getvalue()

    buf = StringIO()
    df.info(buf=buf)
    expected = buf.getvalue()
    assert result == expected

