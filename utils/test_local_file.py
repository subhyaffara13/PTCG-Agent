import os

def test_local_file(all_parsers, csv_dir_path):
    parser = all_parsers
    kwargs = {"sep": "\t"}

    local_path = os.path.join(csv_dir_path, "salaries.csv")
    local_result = parser.read_csv(local_path, **kwargs)
    url = "file://localhost/" + local_path

    try:
        url_result = parser.read_csv(url, **kwargs)
        tm.assert_frame_equal(url_result, local_result)
    except URLError:
        # Fails on some systems.
        pytest.skip("Failing on: " + " ".join(platform.uname()))

