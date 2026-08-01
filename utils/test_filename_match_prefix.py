
def test_filename_match_prefix():
    name_expr = [ ("foo", [2*x, 3*y]), ("bar", [y**2, 4*y]) ]
    result, = codegen(name_expr, "Rust", prefix="baz", header=False,
                     empty=False)
    assert result[0] == "baz.rs"

