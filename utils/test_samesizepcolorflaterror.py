
def test_samesizepcolorflaterror():
    fig, ax = plt.subplots()
    x, y = np.meshgrid(np.arange(5), np.arange(3))
    Z = x + y
    with pytest.raises(TypeError, match=r".*one smaller than X"):
        ax.pcolormesh(x, y, Z, shading='flat')

