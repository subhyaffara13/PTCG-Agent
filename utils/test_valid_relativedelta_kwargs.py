
def test_valid_relativedelta_kwargs(kwd, request):
    if kwd == "millisecond":
        request.applymarker(
            pytest.mark.xfail(
                raises=NotImplementedError,
                reason="Constructing DateOffset object with `millisecond` is not "
                "yet supported.",
            )
        )
    # Check that all the arguments specified in liboffsets._relativedelta_kwds
    # are in fact valid relativedelta keyword args
    DateOffset(**{kwd: 1})

