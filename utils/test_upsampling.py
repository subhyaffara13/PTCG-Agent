
def test_upsampling():

    np.random.seed(19680801+9)  # need this seed to get yellow next to blue
    a = np.random.rand(4, 4)

    fig, axs = plt.subplots(1, 3, figsize=(6.5, 3), layout='compressed')
    im = axs[0].imshow(a, cmap='viridis')
    axs[0].set_title(
        "interpolation='auto'\nstage='antialaised'\n(default for upsampling)")

    # probably what people want:
    axs[1].imshow(a, cmap='viridis', interpolation='sinc')
    axs[1].set_title(
        "interpolation='sinc'\nstage='auto'\n(default for upsampling)")

    # probably not what people want:
    axs[2].imshow(a, cmap='viridis', interpolation='sinc', interpolation_stage='rgba')
    axs[2].set_title("interpolation='sinc'\nstage='rgba'")
    fig.colorbar(im, ax=axs, shrink=0.7, extend='both')

