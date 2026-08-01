
def test_imshow_pil(fig_test, fig_ref):
    style.use("default")
    png_path = Path(__file__).parent / "baseline_images/pngsuite/basn3p04.png"
    tiff_path = Path(__file__).parent / "baseline_images/test_image/uint16.tif"
    axs = fig_test.subplots(2)
    axs[0].imshow(Image.open(png_path))
    axs[1].imshow(Image.open(tiff_path))
    axs = fig_ref.subplots(2)
    axs[0].imshow(plt.imread(png_path))
    axs[1].imshow(plt.imread(tiff_path))

