
def test_path_clipping():
    fig = plt.figure(figsize=(6.0, 6.2))

    for i, xy in enumerate([
            [(200, 200), (200, 350), (400, 350), (400, 200)],
            [(200, 200), (200, 350), (400, 350), (400, 100)],
            [(200, 100), (200, 350), (400, 350), (400, 100)],
            [(200, 100), (200, 415), (400, 350), (400, 100)],
            [(200, 100), (200, 415), (400, 415), (400, 100)],
            [(200, 415), (400, 415), (400, 100), (200, 100)],
            [(400, 415), (400, 100), (200, 100), (200, 415)]]):
        ax = fig.add_subplot(4, 2, i+1)
        bbox = [0, 140, 640, 260]
        ax.set_xlim(bbox[0], bbox[0] + bbox[2])
        ax.set_ylim(bbox[1], bbox[1] + bbox[3])
        ax.add_patch(Polygon(
            xy, facecolor='none', edgecolor='red', closed=True))

