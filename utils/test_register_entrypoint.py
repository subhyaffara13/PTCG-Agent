
def test_register_entrypoint(restore_backend, tmp_path, monkeypatch, dummy_backend):
    monkeypatch.syspath_prepend(tmp_path)
    monkeypatch.setitem(sys.modules, "pandas_dummy_backend", dummy_backend)

    dist_info = tmp_path / "my_backend-0.0.0.dist-info"
    dist_info.mkdir()
    # entry_point name should not match module name - otherwise pandas will
    # fall back to backend lookup by module name
    (dist_info / "entry_points.txt").write_bytes(
        b"[pandas_plotting_backends]\nmy_ep_backend = pandas_dummy_backend\n"
    )

    assert pandas.plotting._core._get_plot_backend("my_ep_backend") is dummy_backend

    with pandas.option_context("plotting.backend", "my_ep_backend"):
        assert pandas.plotting._core._get_plot_backend() is dummy_backend

