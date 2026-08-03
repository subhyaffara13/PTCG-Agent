import sys
from pathlib import Path


def test_verbose():
    # Smoke test that checks the printing does something and does not crash
    x = np.linspace(0, 1, 5)
    y = np.zeros((2, x.shape[0]))
    for verbose in [0, 1, 2]:
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            sol = solve_bvp(exp_fun, exp_bc, x, y, verbose=verbose)
            text = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        assert_(sol.success)
        if verbose == 0:
            assert_(not text, text)
        if verbose >= 1:
            assert_("Solved in" in text, text)
        if verbose >= 2:
            assert_("Max residual" in text, text)


def test_verbose(capfd, hello_world_f90, monkeypatch):
    """Increase verbosity

    CLI :: --verbose
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -m blah {ipath} --verbose'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert "analyzeline" in out

