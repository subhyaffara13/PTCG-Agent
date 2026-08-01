
def capturing_output(request: SubRequest) -> Iterator[Captured]:
    option = request.config.getoption("capture", None)

    capman = request.config.pluginmanager.getplugin("capturemanager")
    if getattr(capman, "_capture_fixture", None):
        # capsys or capfd are active, subtest should not capture.
        fixture = None
    elif option == "sys":
        fixture = CaptureFixture(SysCapture, request, _ispytest=True)
    elif option == "fd":
        fixture = CaptureFixture(FDCapture, request, _ispytest=True)
    else:
        fixture = None

    if fixture is not None:
        fixture._start()

    captured = Captured()
    try:
        yield captured
    finally:
        if fixture is not None:
            out, err = fixture.readouterr()
            fixture.close()
            captured.out = out
            captured.err = err

