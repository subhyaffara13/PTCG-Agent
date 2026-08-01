
def check_disabled(request):
    if getattr(request.module, "disabled", False):
        pytest.skip("test requirements not met.")
    elif getattr(request.module, "ipython", False):
        # need to check version and options for ipython tests
        if (
            version_tuple(pytest.__version__) < version_tuple("2.6.3")
            and pytest.config.getvalue("-s") != "no"
        ):
            pytest.skip("run py.test with -s or upgrade to newer version.")

