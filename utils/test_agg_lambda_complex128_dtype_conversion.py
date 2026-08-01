
def test_agg_lambda_complex128_dtype_conversion():
    # GH#59601
    df = DataFrame(
        {"A": ["c1", "c2", "c3"], "B": pd.array([100, 200, 255], "int64[pyarrow]")}
    )
    gb = df.groupby("A")
    result = gb.agg(lambda x: complex(x.sum(), x.count()))

    expected = DataFrame(
        {
            "B": pd.array(
                [complex(100, 1), complex(200, 1), complex(255, 1)], dtype="complex128"
            ),
        },
        index=Index(["c1", "c2", "c3"], name="A"),
    )
    tm.assert_frame_equal(result, expected)

