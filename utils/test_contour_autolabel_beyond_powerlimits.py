
def test_contour_autolabel_beyond_powerlimits():
    ax = plt.figure().add_subplot()
    cs = plt.contour(np.geomspace(1e-6, 1e-4, 100).reshape(10, 10),
                     levels=[.25e-5, 1e-5, 4e-5])
    ax.clabel(cs)
    # Currently, the exponent is missing, but that may be fixed in the future.
    assert {text.get_text() for text in ax.texts} == {"0.25", "1.00", "4.00"}

