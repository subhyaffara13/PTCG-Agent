
def fp(request):
    if not _HAVE_FASTPARQUET:
        pytest.skip("fastparquet is not installed")
    if using_string_dtype():
        request.applymarker(
            pytest.mark.xfail(reason="TODO(infer_string) fastparquet", strict=False)
        )
    return "fastparquet"

