
def xfail_datetimes_with_pyxlsb(engine, request):
    if engine == "pyxlsb":
        request.applymarker(
            pytest.mark.xfail(
                reason="Sheets containing datetimes not supported by pyxlsb"
            )
        )

