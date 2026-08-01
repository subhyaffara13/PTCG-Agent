
def test_no_interpolation_origin():
    fig, axs = plt.subplots(2)
    axs[0].imshow(np.arange(100).reshape((2, 50)), origin="lower",
                  interpolation='none')
    axs[1].imshow(np.arange(100).reshape((2, 50)), interpolation='none')

