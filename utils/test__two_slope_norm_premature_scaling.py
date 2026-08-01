
def test_TwoSlopeNorm_premature_scaling():
    norm = mcolors.TwoSlopeNorm(vcenter=2)
    with pytest.raises(ValueError):
        norm.inverse(np.array([0.1, 0.5, 0.9]))

