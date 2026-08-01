
def test_multithreaded_reading():
    def numpy_assert(data, b):
        b.wait()
        tm.assert_almost_equal((data + 1) - 1, data.copy())

    tm.run_multithreaded(
        numpy_assert, max_workers=8, arguments=(get_longley_data(),), pass_barrier=True
    )

    def safe_is_const(s):
        try:
            return np.ptp(s) == 0.0 and np.any(s != 0.0)
        except Exception:
            return False

    def concat(data, b):
        b.wait()
        x = data.copy()
        nobs = len(x)
        trendarr = np.fliplr(np.vander(np.arange(1, nobs + 1, dtype=np.float64), 1))
        x.apply(safe_is_const, 0)
        trendarr = DataFrame(trendarr, index=x.index, columns=["const"])
        x = [trendarr, x]
        x = pd.concat(x[::1], axis=1)
        tm.assert_frame_equal(x, x)

    tm.run_multithreaded(
        concat, max_workers=8, arguments=(get_longley_data(),), pass_barrier=True
    )

