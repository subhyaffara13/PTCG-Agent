
def test_imshow_bignumbers():
    rcParams['image.interpolation'] = 'nearest'
    # putting a big number in an array of integers shouldn't
    # ruin the dynamic range of the resolved bits.
    fig, ax = plt.subplots()
    img = np.array([[1, 2, 1e12], [3, 1, 4]], dtype=np.uint64)
    pc = ax.imshow(img)
    pc.set_clim(0, 5)

