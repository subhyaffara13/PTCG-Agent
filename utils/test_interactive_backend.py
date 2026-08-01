
def test_interactive_backend(env, toolbar):
    if env["MPLBACKEND"] == "macosx":
        if toolbar == "toolmanager":
            pytest.skip("toolmanager is not implemented for macosx.")
    if env["MPLBACKEND"] == "wx":
        pytest.skip("wx backend is deprecated; tests failed on appveyor")
    if env["MPLBACKEND"] == "wxagg" and toolbar == "toolmanager":
        pytest.skip("Temporarily deactivated: show() changes figure height "
                    "and thus fails the test")
    try:
        proc = _run_helper(
            _test_interactive_impl,
            json.dumps({"toolbar": toolbar}),
            timeout=_test_timeout,
            extra_env=env,
        )
    except subprocess.CalledProcessError as err:
        pytest.fail(
            "Subprocess failed to test intended behavior\n"
            + str(err.stderr))
    assert proc.stdout.count("CloseEvent") == 1

