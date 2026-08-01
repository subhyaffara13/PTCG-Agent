
def test_diophantine_overflow():
    # Smoke test integer overflow detection
    max_intp = np.iinfo(np.intp).max
    max_int64 = np.iinfo(np.int64).max

    if max_int64 <= max_intp:
        # Check that the algorithm works internally in 128-bit;
        # solving this problem requires large intermediate numbers
        A = (max_int64 // 2, max_int64 // 2 - 10)
        U = (max_int64 // 2, max_int64 // 2 - 10)
        b = 2 * (max_int64 // 2) - 10

        assert_equal(solve_diophantine(A, U, b), (1, 1))

