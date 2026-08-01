
def test_fontcache_thread_safe():
    pytest.importorskip('threading')

    subprocess_run_helper(_test_threading, timeout=10)

