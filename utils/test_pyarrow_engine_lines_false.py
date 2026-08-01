
def test_pyarrow_engine_lines_false():
    # GH 48893
    ser = Series(range(1))
    out = ser.to_json()
    with pytest.raises(ValueError, match="currently pyarrow engine only supports"):
        read_json(out, engine="pyarrow", lines=False)

