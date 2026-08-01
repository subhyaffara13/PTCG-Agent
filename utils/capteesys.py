
def capteesys(request: SubRequest) -> Generator[CaptureFixture[str]]:
    r"""Enable simultaneous text capturing and pass-through of writes
    to ``sys.stdout`` and ``sys.stderr`` as defined by ``--capture=``.


    The captured output is made available via ``capteesys.readouterr()`` method
    calls, which return a ``(out, err)`` namedtuple.
    ``out`` and ``err`` will be ``text`` objects.

    The output is also passed-through, allowing it to be "live-printed",
    reported, or both as defined by ``--capture=``.

    Returns an instance of :class:`CaptureFixture[str] <pytest.CaptureFixture>`.

    Example:

    .. code-block:: python

        def test_output(capteesys):
            print("hello")
            captured = capteesys.readouterr()
            assert captured.out == "hello\n"
    """
    capman: CaptureManager = request.config.pluginmanager.getplugin("capturemanager")
    capture_fixture = CaptureFixture(
        SysCapture, request, config=dict(tee=True), _ispytest=True
    )
    capman.set_fixture(capture_fixture)
    capture_fixture._start()
    yield capture_fixture
    capture_fixture.close()
    capman.unset_fixture()

