
def test_imshow_bignumbers_real():
    rcParams['image.interpolation'] = 'nearest'
    # putting a big number in an array of integers shouldn't
    # ruin the dynamic range of the resolved bits.
    fig, ax = plt.subplots()
    img = np.array([[2., 1., 1.e22], [4., 1., 3.]])
    pc = ax.imshow(img)
    pc.set_clim(0, 5)

