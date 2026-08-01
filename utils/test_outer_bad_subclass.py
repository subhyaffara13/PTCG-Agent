
def test_outer_bad_subclass():
    class BadArr1(np.ndarray):
        def __array_finalize__(self, obj):
            # The outer call reshapes to 3 dims, try to do a bad reshape.
            if self.ndim == 3:
                self._set_shape(self.shape + (1,))

    class BadArr2(np.ndarray):
        def __array_finalize__(self, obj):
            if isinstance(obj, BadArr2):
                # outer inserts 1-sized dims. In that case disturb them.
                if self.shape[-1] == 1:
                    self._set_shape(self.shape[::-1])

    for cls in [BadArr1, BadArr2]:
        arr = np.ones((2, 3)).view(cls)
        with pytest.raises(TypeError):
            # The first array gets reshaped (not the second one)
            np.add.outer(arr, [1, 2])

        # This actually works, since we only see the reshaping error:
        arr = np.ones((2, 3)).view(cls)
        assert type(np.add.outer([1, 2], arr)) is cls

