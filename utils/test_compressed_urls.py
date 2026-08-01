
def test_compressed_urls(
    httpserver,
    datapath,
    salaries_table,
    mode,
    engine,
    compression_only,
    compression_to_extension,
):
    # test reading compressed urls with various engines and
    # extension inference
    if compression_only == "tar":
        pytest.skip("TODO: Add tar salaries.csv to pandas/io/parsers/data")

    extension = compression_to_extension[compression_only]
    with open(datapath("io", "parser", "data", "salaries.csv" + extension), "rb") as f:
        httpserver.serve_content(content=f.read())

    url = httpserver.url + "/salaries.csv" + extension

    if mode != "explicit":
        compression_only = mode

    url_table = read_csv(url, sep="\t", compression=compression_only, engine=engine)
    tm.assert_frame_equal(url_table, salaries_table)

