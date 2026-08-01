
def test_engine_kwargs_append_reader(datapath, ext, kwarg_name, kwarg_value):
    # GH 55027
    # test that `read_only` and `data_only` can be passed to
    #  `openpyxl.reader.excel.load_workbook` via `engine_kwargs`
    filename = datapath("io", "data", "excel", "test1" + ext)
    with contextlib.closing(
        OpenpyxlReader(filename, engine_kwargs={kwarg_name: kwarg_value})
    ) as reader:
        assert getattr(reader.book, kwarg_name) == kwarg_value

