import os
from pathlib import Path


def test_close_file_handle_on_invalid_usecols(all_parsers, temp_file):
    # GH 45384
    parser = all_parsers

    error = ValueError
    if parser.engine == "pyarrow":
        # Raises pyarrow.lib.ArrowKeyError
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    fname = temp_file
    Path(fname).write_text("col1,col2\na,b\n1,2", encoding="utf-8")
    with tm.assert_produces_warning(False):
        with pytest.raises(error, match="col3"):
            parser.read_csv(fname, usecols=["col1", "col2", "col3"])
    # unlink fails on windows if file handles still point to it
    os.unlink(fname)

