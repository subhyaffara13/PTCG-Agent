
def test_align_vectors_antiparallel(xp):
    dtype = xpx.default_dtype(xp)
    # Test exact 180 deg rotation
    atol = 1e-12 if dtype == xp.float64 else 1e-7

    as_to_test = np.array([[[1.0, 0, 0], [0, 1, 0]],
                           [[0, 1, 0], [1, 0, 0]],
                           [[0, 0, 1], [0, 1, 0]]])

    bs_to_test = np.array([[-a[0], a[1]] for a in as_to_test])
    for a, b in zip(as_to_test, bs_to_test):
        a, b = xp.asarray(a, dtype=dtype), xp.asarray(b, dtype=dtype)
        R, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 1])
        xp_assert_close(R.magnitude(), xp.asarray(xp.pi)[()], atol=atol)
        xp_assert_close(R.apply(b[0, ...]), a[0, ...], atol=atol)

    # Test exact rotations near 180 deg
    Rs = Rotation.random(100, rng=0)
    dRs = Rotation.from_rotvec(Rs.as_rotvec()*1e-4)  # scale down to small angle
    a = [[ 1, 0, 0], [0, 1, 0]]
    b = [[-1, 0, 0], [0, 1, 0]]
    as_to_test = []
    for dR in dRs:
        as_to_test.append(np.array([dR.apply(a[0]), a[1]]))

    # GPU computations may be less accurate. See e.g.
    # https://github.com/jax-ml/jax/issues/18934 and
    # https://docs.pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html
    # We currently have no unified way to check which device is being used. Cupy will
    # always run on the GPU regardless of SCIPY_DEVICE, hence the explicit check for
    # cupy. Note that the current implementation lets other frameworks, e.g. numpy, run
    # on the CPU regardless of SCIPY_DEVICE but with increased GPU tolerances.
    if xp_device_type(xp.asarray(0)) == "cuda":
        atol = 1e-7

    for a in as_to_test:
        a, b = xp.asarray(a), xp.asarray(b)
        R, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 1])
        R2, _ = Rotation.align_vectors(a, b, weights=[1e10, 1])
        xp_assert_close(R.as_matrix(), R2.as_matrix(), atol=atol)

