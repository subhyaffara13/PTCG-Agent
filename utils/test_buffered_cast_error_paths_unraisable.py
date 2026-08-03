import subprocess
import sys

def test_buffered_cast_error_paths_unraisable():
    # The following gives an unraisable error. Pytest sometimes captures that
    # (depending python and/or pytest version). So with Python>=3.8 this can
    # probably be cleaned out in the future to check for
    # pytest.PytestUnraisableExceptionWarning:
    code = textwrap.dedent("""
        import numpy as np

        it = np.nditer((np.array(1, dtype="i"),), op_dtypes=["S1"],
                       op_flags=["writeonly"], casting="unsafe", flags=["buffered"])
        buf = next(it)
        buf[...] = "a"
        del buf, it  # Flushing only happens during deallocate right now.
        """)
    res = subprocess.check_output([sys.executable, "-c", code],
                                  stderr=subprocess.STDOUT, text=True)
    assert "ValueError" in res

