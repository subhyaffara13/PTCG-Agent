
def test_norm_abc():

    class CustomHalfNorm(mcolors.Norm):
        def __init__(self):
            super().__init__()

        @property
        def vmin(self):
            return 0

        @property
        def vmax(self):
            return 1

        @property
        def clip(self):
            return False

        def __call__(self, value, clip=None):
            return value / 2

        def inverse(self, value):
            return 2 * value

        def autoscale(self, A):
            pass

        def autoscale_None(self, A):
            pass

        def scaled(self):
            return True

        @property
        def n_components(self):
            return 1

    fig, axes = plt.subplots(2,2)

    r = np.linspace(-1, 3, 16*16).reshape((16,16))
    norm = CustomHalfNorm()
    colorizer = mpl.colorizer.Colorizer(cmap='viridis', norm=norm)
    c = axes[0,0].imshow(r, colorizer=colorizer)
    axes[0,1].pcolor(r, colorizer=colorizer)
    axes[1,0].contour(r, colorizer=colorizer)
    axes[1,1].contourf(r, colorizer=colorizer)

