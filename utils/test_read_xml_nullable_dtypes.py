
def test_read_xml_nullable_dtypes(
    parser, string_storage, dtype_backend, using_infer_string
):
    # GH#50500
    data = """<?xml version='1.0' encoding='utf-8'?>
<data xmlns="http://example.com">
<row>
  <a>x</a>
  <b>1</b>
  <c>4.0</c>
  <d>x</d>
  <e>2</e>
  <f>4.0</f>
  <g></g>
  <h>True</h>
  <i>False</i>
</row>
<row>
  <a>y</a>
  <b>2</b>
  <c>5.0</c>
  <d></d>
  <e></e>
  <f></f>
  <g></g>
  <h>False</h>
  <i></i>
</row>
</data>"""

    with pd.option_context("mode.string_storage", string_storage):
        result = read_xml(StringIO(data), parser=parser, dtype_backend=dtype_backend)

    if dtype_backend == "pyarrow":
        pa = pytest.importorskip("pyarrow")
        string_dtype = pd.ArrowDtype(pa.string())
    else:
        string_dtype = pd.StringDtype(string_storage)

    expected = DataFrame(
        {
            "a": Series(["x", "y"], dtype=string_dtype),
            "b": Series([1, 2], dtype="Int64"),
            "c": Series([4.0, 5.0], dtype="Float64"),
            "d": Series(["x", None], dtype=string_dtype),
            "e": Series([2, NA], dtype="Int64"),
            "f": Series([4.0, NA], dtype="Float64"),
            "g": Series([NA, NA], dtype="Int64"),
            "h": Series([True, False], dtype="boolean"),
            "i": Series([False, NA], dtype="boolean"),
        }
    )

    if dtype_backend == "pyarrow":
        pa = pytest.importorskip("pyarrow")
        from pandas.arrays import ArrowExtensionArray

        expected = DataFrame(
            {
                col: ArrowExtensionArray(pa.array(expected[col], from_pandas=True))
                for col in expected.columns
            }
        )
        expected["g"] = ArrowExtensionArray(pa.array([None, None]))

    # the storage of the str columns' Index is also affected by the
    # string_storage setting -> ignore that for checking the result
    tm.assert_frame_equal(result, expected, check_column_type=False)

