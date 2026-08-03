import functools
import os
import subprocess
import sys

def _isolated_tk_test(success_count, func=None):
    """
    A decorator to run *func* in a subprocess and assert that it prints
    "success" *success_count* times and nothing on stderr.

    TkAgg tests seem to have interactions between tests, so isolate each test
    in a subprocess. See GH#18261
    """

    if func is None:
        return functools.partial(_isolated_tk_test, success_count)

    if "MPL_TEST_ESCAPE_HATCH" in os.environ:
        # set in subprocess_run_helper() below
        return func

    @pytest.mark.skipif(
        not importlib.util.find_spec('tkinter'),
        reason="missing tkinter"
    )
    @pytest.mark.skipif(
        sys.platform == "linux" and not _c_internal_utils.xdisplay_is_valid(),
        reason="$DISPLAY is unset"
    )
    @pytest.mark.xfail(  # https://github.com/actions/setup-python/issues/649
        ('TF_BUILD' in os.environ or 'GITHUB_ACTION' in os.environ) and
        sys.platform == 'darwin' and sys.version_info[:2] < (3, 11),
        reason='Tk version mismatch on Azure macOS CI'
    )
    @functools.wraps(func)
    def test_func():
        # even if the package exists, may not actually be importable this can
        # be the case on some CI systems.
        pytest.importorskip('tkinter')
        try:
            proc = subprocess_run_helper(
                func, timeout=_test_timeout, extra_env=dict(
                    MPLBACKEND="TkAgg", MPL_TEST_ESCAPE_HATCH="1"))
        except subprocess.TimeoutExpired:
            pytest.fail("Subprocess timed out")
        except subprocess.CalledProcessError as e:
            pytest.fail("Subprocess failed to test intended behavior\n"
                        + str(e.stderr))
        else:
            # macOS may actually emit irrelevant errors about Accelerated
            # OpenGL vs. software OpenGL, or some permission error on Azure, so
            # suppress them.
            # Asserting stderr first (and printing it on failure) should be
            # more helpful for debugging that printing a failed success count.
            ignored_lines = ["OpenGL", "CFMessagePort: bootstrap_register",
                             "/usr/include/servers/bootstrap_defs.h"]
            assert not [line for line in proc.stderr.splitlines()
                        if all(msg not in line for msg in ignored_lines)]
            assert proc.stdout.count("success") == success_count

    return test_func

