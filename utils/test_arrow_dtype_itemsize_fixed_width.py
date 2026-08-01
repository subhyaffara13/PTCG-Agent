
def test_arrow_dtype_itemsize_fixed_width(type_name, expected_size):
    # GH 57948

    parametric_type_map = {
        "timestamp": pa.timestamp("ns"),
        "time32": pa.time32("s"),
        "time64": pa.time64("ns"),
        "decimal128": pa.decimal128(38, 10),
        "decimal256": pa.decimal256(76, 10),
    }

    if type_name in parametric_type_map:
        arrow_type = parametric_type_map.get(type_name)
    else:
        arrow_type = getattr(pa, type_name)()
    dtype = ArrowDtype(arrow_type)

    if type_name == "bool_":
        expected_size = dtype.numpy_dtype.itemsize

    assert dtype.itemsize == expected_size, (
        f"{type_name} expected {expected_size}, got {dtype.itemsize} "
        f"(bit_width={getattr(dtype.pyarrow_dtype, 'bit_width', 'N/A')})"
    )

