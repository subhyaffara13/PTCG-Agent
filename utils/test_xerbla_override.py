
def test_xerbla_override():
    # Check that our xerbla has been successfully linked in. If it is not,
    # the default xerbla routine is called, which prints a message to stdout
    # and may, or may not, abort the process depending on the LAPACK package.

    XERBLA_OK = 255

    try:
        pid = os.fork()
    except (OSError, AttributeError):
        # fork failed, or not running on POSIX
        pytest.skip("Not POSIX or fork failed.")

    if pid == 0:
        # child; close i/o file handles
        os.close(1)
        os.close(0)
        # Avoid producing core files.
        import resource
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        # These calls may abort.
        try:
            np.linalg.lapack_lite.xerbla()
        except ValueError:
            pass
        except Exception:
            os._exit(os.EX_CONFIG)

        try:
            a = np.array([[1.]])
            np.linalg.lapack_lite.dorgqr(
                1, 1, 1, a,
                0,  # <- invalid value
                a, a, 0, 0)
        except ValueError as e:
            if "DORGQR parameter number 5" in str(e):
                # success, reuse error code to mark success as
                # FORTRAN STOP returns as success.
                os._exit(XERBLA_OK)

        # Did not abort, but our xerbla was not linked in.
        os._exit(os.EX_CONFIG)
    else:
        # parent
        pid, status = os.wait()
        if os.WEXITSTATUS(status) != XERBLA_OK:
            pytest.skip('Numpy xerbla not linked in.')

