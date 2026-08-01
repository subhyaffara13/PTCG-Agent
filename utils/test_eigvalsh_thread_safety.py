
def test_eigvalsh_thread_safety():
    # if lapack isn't thread safe this will randomly segfault or error
    # see gh-24512
    rng = np.random.RandomState(873699172)
    matrices = (
        rng.random((5, 10, 10, 3, 3)),
        rng.random((5, 10, 10, 3, 3)),
    )

    run_threaded(lambda i: np.linalg.eigvalsh(matrices[i]), 2,
                 pass_count=True)

