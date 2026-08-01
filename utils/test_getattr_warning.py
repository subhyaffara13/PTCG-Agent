
def test_getattr_warning():
    # issue gh-14735: make sure we clear only getattr errors, and let warnings
    # through
    class Wrapper:
        def __init__(self, array):
            self.array = array

        def __len__(self):
            return len(self.array)

        def __getitem__(self, item):
            return type(self)(self.array[item])

        def __getattr__(self, name):
            if name.startswith("__array_"):
                warnings.warn("object got converted", UserWarning, stacklevel=1)

            return getattr(self.array, name)

        def __repr__(self):
            return f"<Wrapper({self.array})>"

    array = Wrapper(np.arange(10))
    with pytest.raises(UserWarning, match="object got converted"):
        np.asarray(array)

