from pathlib import Path


def test_custom_transform():
    plt.rcParams.update({"xtick.direction": "in", "ytick.direction": "inout"})

    class MyTransform(Transform):
        input_dims = output_dims = 2

        def __init__(self, resolution):
            """
            Resolution is the number of steps to interpolate between each input
            line segment to approximate its path in transformed space.
            """
            Transform.__init__(self)
            self._resolution = resolution

        def transform(self, ll):
            x, y = ll.T
            return np.column_stack([x, y - x])

        transform_non_affine = transform

        def transform_path(self, path):
            ipath = path.interpolated(self._resolution)
            return Path(self.transform(ipath.vertices), ipath.codes)

        transform_path_non_affine = transform_path

        def inverted(self):
            return MyTransformInv(self._resolution)

    class MyTransformInv(Transform):
        input_dims = output_dims = 2

        def __init__(self, resolution):
            Transform.__init__(self)
            self._resolution = resolution

        def transform(self, ll):
            x, y = ll.T
            return np.column_stack([x, y + x])

        def inverted(self):
            return MyTransform(self._resolution)

    fig = plt.figure()

    SubplotHost = host_axes_class_factory(Axes)

    tr = MyTransform(1)
    grid_helper = GridHelperCurveLinear(tr)
    ax1 = SubplotHost(fig, 1, 1, 1, grid_helper=grid_helper)
    fig.add_subplot(ax1)

    ax2 = ax1.get_aux_axes(tr, viewlim_mode="equal")
    ax2.plot([3, 6], [5.0, 10.])

    ax1.set_aspect(1.)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)

    ax1.grid(True)

