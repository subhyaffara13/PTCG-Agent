import os

def test_wrong_file_path(parser, geom_df):
    path = "/my/fake/path/output.xml"

    with pytest.raises(
        OSError,
        match=(r"Cannot save file into a non-existent directory: .*path"),
    ):
        geom_df.to_xml(path, parser=parser)


def test_wrong_file_path(parser):
    filename = os.path.join("does", "not", "exist", "books.xml")

    with pytest.raises(
        FileNotFoundError, match=r"\[Errno 2\] No such file or directory"
    ):
        read_xml(filename, parser=parser)

