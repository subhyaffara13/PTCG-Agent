
def test_compression_dict(method, file_ext, tmp_path):
    file_name = f"test.{file_ext}"
    archive_name = "test.dta"
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 2)), columns=list("AB")
    )
    df.index.name = "index"
    compression = {"method": method, "archive_name": archive_name}
    path = tmp_path / file_name
    path.touch()
    df.to_stata(path, compression=compression)
    if method == "zip" or file_ext == "zip":
        with zipfile.ZipFile(path, "r") as zp:
            assert len(zp.filelist) == 1
            assert zp.filelist[0].filename == archive_name
            fp = io.BytesIO(zp.read(zp.filelist[0]))
    else:
        fp = path
    reread = read_stata(fp, index_col="index")

    expected = df
    tm.assert_frame_equal(reread, expected)

