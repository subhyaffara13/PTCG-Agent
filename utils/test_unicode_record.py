
def test_unicode_record(wheel_paths):
    path = next(path for path in wheel_paths if "unicode_dist" in path)
    with ZipFile(path) as zf:
        record = zf.read("unicode_dist-0.1.dist-info/RECORD")

    assert "åäö_日本語.py".encode() in record

