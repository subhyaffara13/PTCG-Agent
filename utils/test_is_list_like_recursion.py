import sys

def test_is_list_like_recursion():
    # GH 33721
    # interpreter would crash with SIGABRT
    def list_like():
        inference.is_list_like([])
        list_like()

    rec_limit = sys.getrecursionlimit()
    try:
        # Limit to avoid stack overflow on Windows CI
        sys.setrecursionlimit(100)
        with tm.external_error_raised(RecursionError):
            list_like()
    finally:
        sys.setrecursionlimit(rec_limit)

