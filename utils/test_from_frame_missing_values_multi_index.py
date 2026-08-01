
def test_from_frame_missing_values_multiIndex():
    # GH 39984
    pa = pytest.importorskip("pyarrow")

    df = pd.DataFrame(
        {
            "a": Series([1, 2, None], dtype="Int64"),
            "b": pd.Float64Dtype().__from_arrow__(pa.array([0.2, None, None])),
        }
    )
    multi_indexed = MultiIndex.from_frame(df)
    expected = MultiIndex.from_arrays(
        [
            Series([1, 2, None], dtype="Int64"),
            pd.Float64Dtype().__from_arrow__(pa.array([0.2, None, None])),
        ],
        names=["a", "b"],
    )
    tm.assert_index_equal(multi_indexed, expected)

