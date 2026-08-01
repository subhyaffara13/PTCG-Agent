
def test_compression(dummy_dist, monkeypatch, tmp_path, option, compress_type):
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path), compression=option).run()
    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        filenames = set(wf.namelist())
        assert "dummy_dist-1.0.dist-info/RECORD" in filenames
        assert "dummy_dist-1.0.dist-info/METADATA" in filenames
        for zinfo in wf.filelist:
            assert zinfo.compress_type == compress_type


def test_compression():
    arr = np.zeros(100).reshape((5,20))
    arr[2,10] = 1
    stream = BytesIO()
    savemat(stream, {'arr':arr})
    raw_len = len(stream.getvalue())
    vals = loadmat(stream)
    assert_array_equal(vals['arr'], arr)
    stream = BytesIO()
    savemat(stream, {'arr':arr}, do_compression=True)
    compressed_len = len(stream.getvalue())
    vals = loadmat(stream)
    assert_array_equal(vals['arr'], arr)
    assert_(raw_len > compressed_len)
    # Concatenate, test later
    arr2 = arr.copy()
    arr2[0,0] = 1
    stream = BytesIO()
    savemat(stream, {'arr':arr, 'arr2':arr2}, do_compression=False)
    vals = loadmat(stream)
    assert_array_equal(vals['arr2'], arr2)
    stream = BytesIO()
    savemat(stream, {'arr':arr, 'arr2':arr2}, do_compression=True)
    vals = loadmat(stream)
    assert_array_equal(vals['arr2'], arr2)


def test_compression(
    compression, version, use_dict, infer, compression_to_extension, tmp_path
):
    file_name = "dta_inferred_compression.dta"
    if compression:
        if use_dict:
            file_ext = compression
        else:
            file_ext = compression_to_extension[compression]
        file_name += f".{file_ext}"
    compression_arg = compression
    if infer:
        compression_arg = "infer"
    if use_dict:
        compression_arg = {"method": compression}

    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 2)), columns=list("AB")
    )
    df.index.name = "index"
    path = tmp_path / file_name
    path.touch()
    df.to_stata(path, version=version, compression=compression_arg)
    if compression == "gzip":
        with gzip.open(path, "rb") as comp:
            fp = io.BytesIO(comp.read())
    elif compression == "zip":
        with zipfile.ZipFile(path, "r") as comp:
            fp = io.BytesIO(comp.read(comp.filelist[0]))
    elif compression == "tar":
        with tarfile.open(path) as tar:
            fp = io.BytesIO(tar.extractfile(tar.getnames()[0]).read())
    elif compression == "bz2":
        with bz2.open(path, "rb") as comp:
            fp = io.BytesIO(comp.read())
    elif compression == "zstd":
        zstd = pytest.importorskip("zstandard")
        with zstd.open(path, "rb") as comp:
            fp = io.BytesIO(comp.read())
    elif compression == "xz":
        lzma = pytest.importorskip("lzma")
        with lzma.open(path, "rb") as comp:
            fp = io.BytesIO(comp.read())
    elif compression is None:
        fp = path
    reread = read_stata(fp, index_col="index")

    expected = df
    tm.assert_frame_equal(reread, expected)


def test_compression(
    tmp_path,
    request,
    parser_and_data,
    compression_only,
    buffer,
    filename,
    compression_to_extension,
):
    parser, data, expected = parser_and_data
    compress_type = compression_only

    ext = compression_to_extension[compress_type]
    filename = filename if filename is None else filename.format(ext=ext)

    if filename and buffer:
        request.applymarker(
            pytest.mark.xfail(
                reason="Cannot deduce compression from buffer of compressed data."
            )
        )

    path = tmp_path / filename if filename else tmp_path / "test_file"
    tm.write_to_compressed(compress_type, path, data)
    compression = "infer" if filename else compress_type

    if buffer:
        with open(path, "rb") as f:
            result = parser.read_csv(f, compression=compression)
    else:
        result = parser.read_csv(path, compression=compression)

    tm.assert_frame_equal(result, expected)

