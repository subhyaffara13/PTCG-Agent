
def test_alpha_validation(pcfunc):
    # Most of the relevant testing is in test_artist and test_colors.
    fig, ax = plt.subplots()
    pc = getattr(ax, pcfunc)(np.arange(12).reshape((3, 4)))
    with pytest.raises(ValueError, match="^Data array shape"):
        pc.set_alpha([0.5, 0.6])
        pc.update_scalarmappable()

