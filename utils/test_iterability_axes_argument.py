
def test_iterability_axes_argument():

    # This is a regression test for matplotlib/matplotlib#3196. If one of the
    # arguments returned by _as_mpl_axes defines __getitem__ but is not
    # iterable, this would raise an exception. This is because we check
    # whether the arguments are iterable, and if so we try and convert them
    # to a tuple. However, the ``iterable`` function returns True if
    # __getitem__ is present, but some classes can define __getitem__ without
    # being iterable. The tuple conversion is now done in a try...except in
    # case it fails.

    class MyAxes(Axes):
        def __init__(self, *args, myclass=None, **kwargs):
            Axes.__init__(self, *args, **kwargs)

    class MyClass:

        def __getitem__(self, item):
            if item != 'a':
                raise ValueError("item should be a")

        def _as_mpl_axes(self):
            return MyAxes, {'myclass': self}

    fig = plt.figure()
    fig.add_subplot(1, 1, 1, projection=MyClass())
    plt.close(fig)

