
def test_pylab_integration():
    IPython = pytest.importorskip("IPython")
    mpl.testing.subprocess_run_helper(
        IPython.start_ipython,
        "--pylab",
        "-c",
        ";".join((
            "import matplotlib.pyplot as plt",
            "assert plt._REPL_DISPLAYHOOK == plt._ReplDisplayHook.IPYTHON",
        )),
        timeout=60,
    )

