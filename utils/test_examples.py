import os

def test_examples(dtype, irl):
    # Note: atol for complex64 bumped from 1e-4 to 1e-3 due to test failures
    # with BLIS, Netlib, and MKL+AVX512 - see
    # https://github.com/conda-forge/scipy-feedstock/pull/198#issuecomment-999180432
    atol = {
        np.float32: 1.3e-4,
        np.float64: 1e-9,
        np.complex64: 1e-3,
        np.complex128: 1e-9,
    }[dtype]

    path_prefix = os.path.dirname(__file__)
    # Test matrices from `illc1850.coord` and `mhd1280b.cua` distributed with
    # PROPACK 2.1: http://sun.stanford.edu/~rmunk/PROPACK/
    relative_path = "propack_test_data.npz"
    filename = os.path.join(path_prefix, relative_path)
    with np.load(filename, allow_pickle=True) as data:
        if is_complex_type(dtype):
            A = data['A_complex'].item().astype(dtype)
        else:
            A = data['A_real'].item().astype(dtype)

    k = 200
    u, s, vh, _ = _svdp(A, k, irl_mode=irl, rng=np.random.default_rng(0))

    # complex example matrix has many repeated singular values, so check only
    # beginning non-repeated singular vectors to avoid permutations
    sv_check = 27 if is_complex_type(dtype) else k
    u = u[:, :sv_check]
    vh = vh[:sv_check, :]
    s = s[:sv_check]

    # Check orthogonality of singular vectors
    assert_allclose(np.eye(u.shape[1]), u.conj().T @ u, atol=atol)
    assert_allclose(np.eye(vh.shape[0]), vh @ vh.conj().T, atol=atol)

    # Ensure the norm of the difference between the np.linalg.svd and
    # PROPACK reconstructed matrices is small
    u3, s3, vh3 = np.linalg.svd(A.todense())
    u3 = u3[:, :sv_check]
    s3 = s3[:sv_check]
    vh3 = vh3[:sv_check, :]
    A3 = u3 @ np.diag(s3) @ vh3
    recon = u @ np.diag(s) @ vh
    assert_allclose(np.linalg.norm(A3 - recon), 0, atol=atol)

