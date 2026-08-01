
def disable_bottleneck(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(nanops, "_USE_BOTTLENECK", False)
        yield

