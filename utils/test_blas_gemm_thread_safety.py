
def test_blas_gemm_thread_safety():
    # gh-31618: concurrently run transpose and no-transpose GEMM variants to
    # exercise possible thread safety issues due to lock sharding between
    # kernels, see OpenBLAS issue #5836.
    num_threads = 8
    num_iters = 10
    M = 512 * 512

    rng = np.random.default_rng(0x9e3779b9)
    no_trans = rng.random((M, 4))            # C-contiguous -> NoTrans GEMM
    no_trans_w = rng.random((4, 2))
    trans = rng.random((2, M)).T             # F-contiguous -> Trans GEMM
    trans_w = rng.random((2, 2))
    expected_no_trans = no_trans @ no_trans_w
    expected_trans = trans @ trans_w

    mismatches = 0
    lock = threading.Lock()

    def closure(i, b):
        nonlocal mismatches
        count = 0
        for _ in range(num_iters):
            b.wait()
            if i % 2:
                ok = np.array_equal(no_trans @ no_trans_w, expected_no_trans)
            else:
                ok = np.array_equal(trans @ trans_w, expected_trans)
            if not ok:
                count += 1
        with lock:
            mismatches += count

    run_threaded(closure, num_threads, pass_count=True, pass_barrier=True)

    blas_name, blas_version = _detected_blas()
    if mismatches and _openblas_predates_gemm_fix(blas_name, blas_version):
        pytest.xfail(
            f"OpenBLAS version ({blas_version}) predates first OpenBLAS "
            "version with a fix (0.3.33.112)"
        )

    assert mismatches == 0, (
        f"{mismatches} concurrent matmul results were corrupted "
        f"({blas_name} {blas_version})"
    )

