
def test_properties():
    instance = m.TestProperties()

    assert instance.def_readonly == 1
    with pytest.raises(AttributeError):
        instance.def_readonly = 2

    instance.def_readwrite = 2
    assert instance.def_readwrite == 2

    assert instance.def_property_readonly == 2
    with pytest.raises(AttributeError):
        instance.def_property_readonly = 3

    instance.def_property = 3
    assert instance.def_property == 3

    with pytest.raises(AttributeError) as excinfo:
        dummy = instance.def_property_writeonly  # unused var
    assert NO_GETTER_MSG in str(excinfo.value)

    instance.def_property_writeonly = 4
    assert instance.def_property_readonly == 4

    with pytest.raises(AttributeError) as excinfo:
        dummy = instance.def_property_impossible  # noqa: F841 unused var
    assert NO_GETTER_MSG in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        instance.def_property_impossible = 5
    assert NO_SETTER_MSG in str(excinfo.value)


def test_properties():
    R = QQ.old_poly_ring(x, y)
    F = R.free_module(2)
    h = homomorphism(F, F, [[x, 0], [y, 0]])
    assert h.kernel() == F.submodule([-y, x])
    assert h.image() == F.submodule([x, 0], [y, 0])
    assert not h.is_injective()
    assert not h.is_surjective()
    assert h.restrict_codomain(h.image()).is_surjective()
    assert h.restrict_domain(F.submodule([1, 0])).is_injective()
    assert h.quotient_domain(
        h.kernel()).restrict_codomain(h.image()).is_isomorphism()

    R2 = QQ.old_poly_ring(x, y, order=(("lex", x), ("ilex", y))) / [x**2 + 1]
    F = R2.free_module(2)
    h = homomorphism(F, F, [[x, 0], [y, y + 1]])
    assert h.is_isomorphism()


def test_properties(xp, ndim: int):
    atol = 1e-12 if xpx.default_dtype(xp) == xp.float64 else 1e-6
    shape = (ndim,) * (ndim - 1)
    dtype = xpx.default_dtype(xp)
    rng = np.random.default_rng(100)

    # Test rotation and translation properties
    r = Rotation.from_quat(xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype))
    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    tf = RigidTransform.from_components(t, r)

    xp_assert_close(tf.rotation.as_matrix(), r.as_matrix(), atol=atol)
    assert xp.all(tf.rotation.approx_equal(r, atol=atol))
    xp_assert_close(tf.translation, t, atol=atol)
    # Test that we don't return views that would modify the original array
    xpx.at(tf.translation)[..., 0].set(0.0)
    xp_assert_close(tf.translation, t, atol=atol)
    assert tf.single == (shape == ())


def test_properties(m, p, q, swap_sign):
    # Test all the properties advertised in `linalg.cossin` documentation.
    # There may be some overlap with tests above, but this is sensitive to
    # the bug reported in gh-19365 and more.
    if (p >= m) or (q >= m):
        pytest.skip("`0 < p < m` and `0 < q < m` must hold")

    # Generate unitary input
    rng = np.random.default_rng(329548272348596421)
    X = unitary_group.rvs(m, random_state=rng)
    np.testing.assert_allclose(X @ X.conj().T, np.eye(m), atol=1e-15)

    # Perform the decomposition
    u0, cs0, vh0 = linalg.cossin(X, p=p, q=q, separate=True, swap_sign=swap_sign)
    u1, u2 = u0
    v1, v2 = vh0
    v1, v2 = v1.conj().T, v2.conj().T

    # "U1, U2, V1, V2 are square orthogonal/unitary matrices
    # of dimensions (p,p), (m-p,m-p), (q,q), and (m-q,m-q) respectively"
    np.testing.assert_allclose(u1 @ u1.conj().T, np.eye(p), atol=1e-13)
    np.testing.assert_allclose(u2 @ u2.conj().T, np.eye(m-p), atol=1e-13)
    np.testing.assert_allclose(v1 @ v1.conj().T, np.eye(q), atol=1e-13)
    np.testing.assert_allclose(v2 @ v2.conj().T, np.eye(m-q), atol=1e-13)

    # "and C and S are (r, r) nonnegative diagonal matrices..."
    C = np.diag(np.cos(cs0))
    S = np.diag(np.sin(cs0))
    # "...satisfying C^2 + S^2 = I where r = min(p, m-p, q, m-q)."
    r = min(p, m-p, q, m-q)
    np.testing.assert_allclose(C**2 + S**2, np.eye(r))

    # "Moreover, the rank of the identity matrices are
    # min(p, q) - r, min(p, m - q) - r, min(m - p, q) - r,
    # and min(m - p, m - q) - r respectively."
    I11 = np.eye(min(p, q) - r)
    I12 = np.eye(min(p, m - q) - r)
    I21 = np.eye(min(m - p, q) - r)
    I22 = np.eye(min(m - p, m - q) - r)

    # From:
    #                            ┌                   ┐
    #                            │ I  0  0 │ 0  0  0 │
    # ┌           ┐   ┌         ┐│ 0  C  0 │ 0 -S  0 │┌         ┐*
    # │ X11 │ X12 │   │ U1 │    ││ 0  0  0 │ 0  0 -I ││ V1 │    │
    # │ ────┼──── │ = │────┼────││─────────┼─────────││────┼────│
    # │ X21 │ X22 │   │    │ U2 ││ 0  0  0 │ I  0  0 ││    │ V2 │
    # └           ┘   └         ┘│ 0  S  0 │ 0  C  0 │└         ┘
    #                            │ 0  0  I │ 0  0  0 │
    #                            └                   ┘

    # We can see that U and V are block diagonal matrices like so:
    U = linalg.block_diag(u1, u2)
    V = linalg.block_diag(v1, v2)

    # And the center matrix, which we'll call Q here, must be:
    Q11 = np.zeros((u1.shape[1], v1.shape[0]))
    IC11 = linalg.block_diag(I11, C)
    Q11[:IC11.shape[0], :IC11.shape[1]] = IC11

    Q12 = np.zeros((u1.shape[1], v2.shape[0]))
    SI12 = linalg.block_diag(S, I12) if swap_sign else linalg.block_diag(-S, -I12)
    Q12[-SI12.shape[0]:, -SI12.shape[1]:] = SI12

    Q21 = np.zeros((u2.shape[1], v1.shape[0]))
    SI21 = linalg.block_diag(-S, -I21) if swap_sign else linalg.block_diag(S, I21)
    Q21[-SI21.shape[0]:, -SI21.shape[1]:] = SI21

    Q22 = np.zeros((u2.shape[1], v2.shape[0]))
    IC22 = linalg.block_diag(I22, C)
    Q22[:IC22.shape[0], :IC22.shape[1]] = IC22

    Q = np.block([[Q11, Q12], [Q21, Q22]])

    # Confirm that `cossin` decomposes `X` as shown
    np.testing.assert_allclose(X, U @ Q @ V.conj().T)

    # And check that `separate=False` agrees
    U0, CS0, Vh0 = linalg.cossin(X, p=p, q=q, swap_sign=swap_sign)
    np.testing.assert_allclose(U, U0)
    np.testing.assert_allclose(Q, CS0)
    np.testing.assert_allclose(V, Vh0.conj().T)

    # Confirm that `compute_u`/`compute_vh` don't affect the results
    kwargs = dict(p=p, q=q, swap_sign=swap_sign)

    # `compute_u=False`
    u, cs, vh = linalg.cossin(X, separate=True, compute_u=False, **kwargs)
    assert u[0].shape == (0, 0)  # probably not ideal, but this is what it does
    assert u[1].shape == (0, 0)
    assert_allclose(cs, cs0, rtol=1e-15)
    assert_allclose(vh[0], vh0[0], rtol=1e-15)
    assert_allclose(vh[1], vh0[1], rtol=1e-15)

    U, CS, Vh = linalg.cossin(X, compute_u=False, **kwargs)
    assert U.shape == (0, 0)
    assert_allclose(CS, CS0, rtol=1e-15)
    assert_allclose(Vh, Vh0, rtol=1e-15)

    # `compute_vh=False`
    u, cs, vh = linalg.cossin(X, separate=True, compute_vh=False, **kwargs)
    assert_allclose(u[0], u[0], rtol=1e-15)
    assert_allclose(u[1], u[1], rtol=1e-15)
    assert_allclose(cs, cs0, rtol=1e-15)
    assert vh[0].shape == (0, 0)
    assert vh[1].shape == (0, 0)

    U, CS, Vh = linalg.cossin(X, compute_vh=False, **kwargs)
    assert_allclose(U, U0, rtol=1e-15)
    assert_allclose(CS, CS0, rtol=1e-15)
    assert Vh.shape == (0, 0)

    # `compute_u=False, compute_vh=False`
    u, cs, vh = linalg.cossin(X, separate=True, compute_u=False,
                              compute_vh=False, **kwargs)
    assert u[0].shape == (0, 0)
    assert u[1].shape == (0, 0)
    assert_allclose(cs, cs0, rtol=1e-15)
    assert vh[0].shape == (0, 0)
    assert vh[1].shape == (0, 0)

    U, CS, Vh = linalg.cossin(X, compute_u=False, compute_vh=False, **kwargs)
    assert U.shape == (0, 0)
    assert_allclose(CS, CS0, rtol=1e-15)
    assert Vh.shape == (0, 0)


def test_properties():
    ln = mlines.Line2D([], [])
    ln.properties()  # Check that no warning is emitted.

