
def test_engine_kwargs_write(tmp_excel, iso_dates):
    # GH 42286 GH 43445
    engine_kwargs = {"iso_dates": iso_dates}
    with ExcelWriter(
        tmp_excel, engine="openpyxl", engine_kwargs=engine_kwargs
    ) as writer:
        assert writer.book.iso_dates == iso_dates
        # ExcelWriter won't allow us to close without writing something
        DataFrame().to_excel(writer)

