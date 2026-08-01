
def test_shadow_invalid_argument():
    # Test if invalid argument to legend shadow
    # (i.e. not [color|bool]) raises ValueError
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='test')
    with pytest.raises(ValueError, match="dict or bool"):
        ax.legend(loc="upper left", shadow="aardvark")  # Bad argument

