
def test_complex_append(temp_hdfstore):
    df = DataFrame(
        {
            "a": np.random.default_rng(2).standard_normal(100).astype(np.complex128),
            "b": np.random.default_rng(2).standard_normal(100),
        }
    )

    temp_hdfstore.append("df", df, data_columns=["b"])
    temp_hdfstore.append("df", df)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(pd.concat([df, df], axis=0), result)

