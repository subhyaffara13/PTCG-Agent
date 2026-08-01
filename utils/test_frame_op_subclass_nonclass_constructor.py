
def test_frame_op_subclass_nonclass_constructor():
    # GH#43201 subclass._constructor is a function, not the subclass itself

    class SubclassedSeries(Series):
        @property
        def _constructor(self):
            return SubclassedSeries

        @property
        def _constructor_expanddim(self):
            return SubclassedDataFrame

    class SubclassedDataFrame(DataFrame):
        _metadata = ["my_extra_data"]

        def __init__(self, my_extra_data, *args, **kwargs) -> None:
            self.my_extra_data = my_extra_data
            super().__init__(*args, **kwargs)

        @property
        def _constructor(self):
            return functools.partial(type(self), self.my_extra_data)

        @property
        def _constructor_sliced(self):
            return SubclassedSeries

    sdf = SubclassedDataFrame("some_data", {"A": [1, 2, 3], "B": [4, 5, 6]})
    result = sdf * 2
    expected = SubclassedDataFrame("some_data", {"A": [2, 4, 6], "B": [8, 10, 12]})
    tm.assert_frame_equal(result, expected)

    result = sdf + sdf
    tm.assert_frame_equal(result, expected)

