
def test_regularpolycollection_scale():
    # See issue #3860

    class SquareCollection(mcollections.RegularPolyCollection):
        def __init__(self, **kwargs):
            super().__init__(4, rotation=np.pi/4., **kwargs)

        def get_transform(self):
            """Return transform scaling circle areas to data space."""
            ax = self.axes

            pts2pixels = 72.0 / ax.get_figure(root=True).dpi

            scale_x = pts2pixels * ax.bbox.width / ax.viewLim.width
            scale_y = pts2pixels * ax.bbox.height / ax.viewLim.height
            return mtransforms.Affine2D().scale(scale_x, scale_y)

    fig, ax = plt.subplots()

    xy = [(0, 0)]
    # Unit square has a half-diagonal of `1/sqrt(2)`, so `pi * r**2` equals...
    circle_areas = [np.pi / 2]
    squares = SquareCollection(
        sizes=circle_areas, offsets=xy, offset_transform=ax.transData)
    ax.add_collection(squares)
    ax.axis([-1, 1, -1, 1])

