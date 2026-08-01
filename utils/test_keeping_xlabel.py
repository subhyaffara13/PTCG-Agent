
def test_keeping_xlabel():
    # github issue #23398 - xlabels being ignored in colorbar axis
    arr = np.arange(25).reshape((5, 5))
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    cbar = plt.colorbar(im)
    cbar.ax.set_xlabel('Visible Xlabel')
    cbar.set_label('YLabel')

