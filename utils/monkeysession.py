
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp

