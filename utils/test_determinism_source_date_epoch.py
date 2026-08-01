
def test_determinism_source_date_epoch(fmt, string):
    """
    Test SOURCE_DATE_EPOCH support.

    Output a document with the environment variable SOURCE_DATE_EPOCH set to
    2000-01-01 00:00 UTC and check that the document contains the timestamp that
    corresponds to this date (given as an argument).

    Parameters
    ----------
    fmt : {"pdf", "ps", "svg"}
        Output format.
    string : bytes
        Timestamp string for 2000-01-01 00:00 UTC.
    """
    buf = subprocess_run_for_testing(
        [sys.executable, "-R", "-c",
         f"from matplotlib.tests.test_determinism import _save_figure; "
         f"_save_figure('', {fmt!r})"],
        env={**os.environ, "SOURCE_DATE_EPOCH": "946684800",
             "MPLBACKEND": "Agg"}, capture_output=True, text=False, check=True).stdout
    assert string in buf

