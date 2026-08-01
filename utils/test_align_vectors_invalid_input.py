
def test_align_vectors_invalid_input(xp):
    with pytest.raises(ValueError, match="Expected input `a` to have shape"):
        a, b = xp.asarray([1, 2, 3, 4]), xp.asarray([1, 2, 3])
        Rotation.align_vectors(a, b)

    with pytest.raises(ValueError, match="Expected input `b` to have shape"):
        a, b = xp.asarray([1, 2, 3]), xp.asarray([1, 2, 3, 4])
        Rotation.align_vectors(a, b)

    with pytest.raises(ValueError, match="Expected inputs `a` and `b` "
                                         "to have same shapes"):
        a, b = xp.asarray([[1, 2, 3], [4, 5, 6]]), xp.asarray([[1, 2, 3]])
        Rotation.align_vectors(a, b)

    with pytest.raises(ValueError,
                       match="Expected `weights` to be 1 dimensional"):
        a, b = xp.asarray([[1, 2, 3]]), xp.asarray([[1, 2, 3]])
        weights = xp.asarray([[1]])
        Rotation.align_vectors(a, b, weights)

    with pytest.raises(ValueError,
                       match="Expected `weights` to have number of values"):
        a, b = xp.asarray([[1, 2, 3], [4, 5, 6]]), xp.asarray([[1, 2, 3], [4, 5, 6]])
        weights = xp.asarray([1, 2, 3])
        Rotation.align_vectors(a, b, weights)

    a, b = xp.asarray([[1, 2, 3]]), xp.asarray([[1, 2, 3]])
    weights = xp.asarray([-1])
    if is_lazy_array(weights):
        r, rssd = Rotation.align_vectors(a, b, weights)
        assert xp.all(xp.isnan(r.as_quat())), "Quaternion should be nan"
        assert xp.isnan(rssd), "RSSD should be nan"
    else:
        with pytest.raises(ValueError,
                           match="`weights` may not contain negative values"):
            Rotation.align_vectors(a, b, weights)

    a, b = xp.asarray([[1, 2, 3], [4, 5, 6]]), xp.asarray([[1, 2, 3], [4, 5, 6]])
    weights = xp.asarray([xp.inf, xp.inf])
    if is_lazy_array(weights):
        r, rssd = Rotation.align_vectors(a, b, weights)
        assert xp.all(xp.isnan(r.as_quat())), "Quaternion should be nan"
        assert xp.isnan(rssd), "RSSD should be nan"
    else:
        with pytest.raises(ValueError,
                           match="Only one infinite weight is allowed"):
            Rotation.align_vectors(a, b, weights)

    a, b = xp.asarray([[0, 0, 0]]), xp.asarray([[1, 2, 3]])
    if is_lazy_array(a):
        r, rssd = Rotation.align_vectors(a, b)
        assert xp.all(xp.isnan(r.as_quat())), "Quaternion should be nan"
        assert xp.isnan(rssd), "RSSD should be nan"
    else:
        with pytest.raises(ValueError,
                           match="Cannot align zero length primary vectors"):
            Rotation.align_vectors(a, b)

    a, b = xp.asarray([[1, 2, 3], [4, 5, 6]]), xp.asarray([[1, 2, 3], [4, 5, 6]])
    weights = xp.asarray([xp.inf, 1])
    if is_lazy_array(a):
        r, rssd, sens = Rotation.align_vectors(a, b, weights, return_sensitivity=True)
        assert xp.all(xp.isnan(sens)), "Sensitivity matrix should be nan"
    else:
        with pytest.raises(ValueError,
                           match="Cannot return sensitivity matrix"):
            Rotation.align_vectors(a, b, weights, return_sensitivity=True)

    a, b = xp.asarray([[1, 2, 3]]), xp.asarray([[1, 2, 3]])
    if is_lazy_array(a):
        r, rssd, sens = Rotation.align_vectors(a, b, return_sensitivity=True)
        assert xp.all(xp.isnan(sens)), "Sensitivity matrix should be nan"
    else:
        with pytest.raises(ValueError,
                        match="Cannot return sensitivity matrix"):
                        Rotation.align_vectors(a, b, return_sensitivity=True)

    # No broadcast support for align_vectors
    a, b = xp.asarray([[[1, 2, 3]]]), xp.asarray([[[1, 2, 3]]])
    with pytest.raises(ValueError,
                       match="Expected inputs `a` and `b` to have shape"):
        Rotation.align_vectors(a, b)

