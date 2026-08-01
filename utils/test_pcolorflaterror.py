
def test_pcolorflaterror():
    fig, ax = plt.subplots()
    x = np.arange(0, 9)
    y = np.arange(0, 3)
    np.random.seed(19680801)
    Z = np.random.randn(3, 9)
    with pytest.raises(TypeError, match='Dimensions of C'):
        ax.pcolormesh(x, y, Z, shading='flat')

