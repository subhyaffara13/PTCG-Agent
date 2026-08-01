
def check_threadpoolctl():
    try:
        import threadpoolctl
        if not hasattr(threadpoolctl, "register"):
            pytest.skip("threadpoolctl too old")
            return
    except ImportError:
        pytest.skip("no threadpoolctl")
        return

