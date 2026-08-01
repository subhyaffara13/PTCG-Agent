
def test_multi_thread_string_io_read_csv(all_parsers, request):
    # see gh-11786
    parser = all_parsers
    if parser.engine == "pyarrow":
        pa = pytest.importorskip("pyarrow")
        if Version(pa.__version__) < Version("16.0"):
            request.applymarker(
                pytest.mark.xfail(reason="# ValueError: Found non-unique column index")
            )
    max_row_range = 100
    num_files = 10

    bytes_to_df = (
        "\n".join([f"{i:d},{i:d},{i:d}" for i in range(max_row_range)]).encode()
        for _ in range(num_files)
    )

    # Read all files in many threads.
    with ExitStack() as stack:
        files = [stack.enter_context(BytesIO(b)) for b in bytes_to_df]

        pool = stack.enter_context(ThreadPool(8))

        results = pool.map(parser.read_csv, files)
        first_result = results[0]

        for result in results:
            tm.assert_frame_equal(first_result, result)

