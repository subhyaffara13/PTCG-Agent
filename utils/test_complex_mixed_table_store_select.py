
def test_complex_mixed_table_store_select(temp_hdfstore):
    complex64 = np.array(
        [1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j], dtype=np.complex64
    )
    complex128 = np.array(
        [1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j], dtype=np.complex128
    )
    df = DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": ["a", "b", "c", "d"],
            "C": complex64,
            "D": complex128,
            "E": [1.0, 2.0, 3.0, 4.0],
        },
        index=list("abcd"),
    )

    temp_hdfstore.append("df", df, data_columns=["A", "B"])
    result = temp_hdfstore.select("df", where="A>2")
    tm.assert_frame_equal(df.loc[df.A > 2], result)

