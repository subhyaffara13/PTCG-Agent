
def test_zero_norms_from_quat(xp):
    x = xp.asarray([
            [3, 4, 0, 0],
            [0, 0, 0, 0],
            [5, 0, 12, 0]
            ])
    if is_lazy_array(x):
        assert xp.all(xp.isnan(Rotation.from_quat(x).as_quat()[1, ...]))
    else:
        with pytest.raises(ValueError):
            Rotation.from_quat(x)

