
def test_pngsuite():
    files = sorted(
        (Path(__file__).parent / "baseline_images/pngsuite").glob("basn*.png"))

    plt.figure(figsize=(len(files), 2))

    for i, fname in enumerate(files):
        data = plt.imread(fname)
        cmap = None  # use default colormap
        if data.ndim == 2:
            # keep grayscale images gray
            cmap = cm.gray
        plt.imshow(data, extent=(i, i + 1, 0, 1), cmap=cmap, interpolation='nearest')

    plt.gca().patch.set_facecolor("#ddffff")
    plt.gca().set_xlim(0, len(files))

