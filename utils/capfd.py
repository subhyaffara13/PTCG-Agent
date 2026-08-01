
def capfd(request: SubRequest) -> Generator[CaptureFixture[str]]:
    r"""Enable text capturing of writes to file descriptors ``1`` and ``2``.

    The captured output is made available via ``capfd.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    Returns an instance of :class:`CaptureFixture[str] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_system_echo(capfd):
            os.system('echo "hello"')
            captured = capfd.readouterr()
            assert captured.out == "hello\n"
    """
    capman: CaptureManager = request.config.pluginmanager.getplugin("capturemanager")
    capture_fixture = CaptureFixture(FDCapture, request, _ispytest=True)
    capman.set_fixture(capture_fixture)
    capture_fixture._start()
    yield capture_fixture
    capture_fixture.close()
    capman.unset_fixture()

