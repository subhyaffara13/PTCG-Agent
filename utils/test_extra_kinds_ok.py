import sys

def test_extra_kinds_ok(monkeypatch, restore_backend, dummy_backend):
    # https://github.com/pandas-dev/pandas/pull/28647
    monkeypatch.setitem(sys.modules, "pandas_dummy_backend", dummy_backend)
    pandas.set_option("plotting.backend", "pandas_dummy_backend")
    df = pandas.DataFrame({"A": [1, 2, 3]})
    df.plot(kind="not a real kind")

