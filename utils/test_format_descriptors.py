
def test_format_descriptors():
    with pytest.raises(RuntimeError) as excinfo:
        m.get_format_unbound()
    assert re.match(
        "^NumPy type info missing for .*UnboundStruct.*$", str(excinfo.value)
    )

    ld = np.dtype("longdouble")
    ldbl_fmt = ("4x" if ld.alignment > 4 else "") + ld.char
    ss_fmt = "^T{?:bool_:3xI:uint_:f:float_:" + ldbl_fmt + ":ldbl_:}"
    dbl = np.dtype("double")
    end_padding = ld.itemsize % np.dtype("uint64").alignment
    partial_fmt = (
        "^T{?:bool_:3xI:uint_:f:float_:"
        + str(4 * (dbl.alignment > 4) + dbl.itemsize + 8 * (ld.alignment > 8))
        + "xg:ldbl_:"
        + (str(end_padding) + "x}" if end_padding > 0 else "}")
    )
    nested_extra = str(max(8, ld.alignment))
    assert m.print_format_descriptors() == [
        ss_fmt,
        "^T{?:bool_:I:uint_:f:float_:g:ldbl_:}",
        "^T{" + ss_fmt + ":a:^T{?:bool_:I:uint_:f:float_:g:ldbl_:}:b:}",
        partial_fmt,
        "^T{" + nested_extra + "x" + partial_fmt + ":a:" + nested_extra + "x}",
        "^T{3s:a:3s:b:}",
        "^T{(3)4s:a:(2)i:b:(3)B:c:1x(4, 2)f:d:}",
        "^T{q:e1:B:e2:}",
        "^T{Zf:cflt:Zd:cdbl:}",
    ]

