
def test_ewma_times_adjust_false_with_disallowed_alpha():
    # GH 54328
    with pytest.raises(
        NotImplementedError,
        match=(
            "None of com, span, or alpha can be specified "
            "if times is provided and adjust=False"
        ),
    ):
        Series(range(1)).ewm(
            0.1,
            adjust=False,
            times=date_range("2000", freq="D", periods=1),
            alpha=0.5,
            halflife="1D",
        )

