
def test_show(case, capsys, xp, batch_A, batch_b):
    if case.solver != tfqmr:
        pytest.skip("tfqmr specific test")
    if "poisson2d-F" in case.name:
        pytest.skip("Hits divide-by-zero with single precision")
    if "pd-F" in case.name:
        pytest.skip("Struggles to converge with single precision on some platforms")
    case = xp_case(case, xp, batch_A, batch_b)
    def cb(x):
        pass

    ctx = (
        np.errstate(all='ignore')
        if case.casename == "nonsymposdef"
        else nullcontext()
    )
    with ctx:
        x, info = tfqmr(case.A, case.b, callback=cb, show=True)

    out, err = capsys.readouterr()

    if case.casename == "sym-nonpd":
        # no logs for some reason
        exp = ""
    elif case.casename in ("nonsymposdef", "nonsymposdef-F"):
        # Asymmetric and Positive Definite
        exp = "TFQMR: Linear solve not converged due to reach MAXIT iterations"
    else:  # all other cases
        exp = "TFQMR: Linear solve converged due to reach TOL iterations"

    assert out.startswith(exp)
    assert err == ""


def test_show(monkeypatch):
    mpl_test_backend = SimpleNamespace(**vars(backend_template))
    mock_show = MagicMock()
    monkeypatch.setattr(
        mpl_test_backend.FigureManagerTemplate, "pyplot_show", mock_show)
    monkeypatch.setitem(sys.modules, "mpl_test_backend", mpl_test_backend)
    mpl.use("module://mpl_test_backend")
    plt.show()
    mock_show.assert_called_with()

