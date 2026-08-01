
def test_imshow_10_10_2():
    fig, ax = plt.subplots()
    arr = np.arange(200).reshape((10, 10, 2))
    with pytest.raises(TypeError):
        ax.imshow(arr)

