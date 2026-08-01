
def test_engine_kwargs(tmp_excel, engine_kwargs):
    # GH 42286
    # GH 43445
    # test for error: OpenDocumentSpreadsheet does not accept any arguments
    if engine_kwargs is not None:
        error = re.escape(
            "OpenDocumentSpreadsheet() got an unexpected keyword argument 'kwarg'"
        )
        with pytest.raises(
            TypeError,
            match=error,
        ):
            ExcelWriter(tmp_excel, engine="odf", engine_kwargs=engine_kwargs)
    else:
        with ExcelWriter(tmp_excel, engine="odf", engine_kwargs=engine_kwargs) as _:
            pass


def test_engine_kwargs(tmp_excel, nan_inf_to_errors):
    # GH 42286
    engine_kwargs = {"options": {"nan_inf_to_errors": nan_inf_to_errors}}
    with ExcelWriter(
        tmp_excel, engine="xlsxwriter", engine_kwargs=engine_kwargs
    ) as writer:
        assert writer.book.nan_inf_to_errors == nan_inf_to_errors

