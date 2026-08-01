
def test_invalid_index_types(idx):
    # see gh-48439
    msg = "|".join(
        [
            "cannot infer freq from a non-convertible",
            "Check the `freq` attribute instead of using infer_freq",
        ]
    )

    with pytest.raises(TypeError, match=msg):
        frequencies.infer_freq(idx)

