
def _pytest(request: FixtureRequest) -> PytestArg:
    """Return a helper which offers a gethookrecorder(hook) method which
    returns a HookRecorder instance which helps to make assertions about called
    hooks."""
    return PytestArg(request)

