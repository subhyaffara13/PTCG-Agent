
def test_cossin_error_partitioning():
    x = np.array(ortho_group.rvs(4), dtype=np.float64)
    with pytest.raises(ValueError, match="invalid p=0.*0<p<4.*"):
        cossin(x, 0, 1)
    with pytest.raises(ValueError, match="invalid p=4.*0<p<4.*"):
        cossin(x, 4, 1)
    with pytest.raises(ValueError, match="invalid q=-2.*0<q<4.*"):
        cossin(x, 1, -2)
    with pytest.raises(ValueError, match="invalid q=5.*0<q<4.*"):
        cossin(x, 1, 5)

