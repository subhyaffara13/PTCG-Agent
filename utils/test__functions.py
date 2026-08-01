
def test_Functions():
    assert rust_code(sin(x) ** cos(x)) == "x.sin().powf(x.cos())"
    assert rust_code(abs(x)) == "x.abs()"
    assert rust_code(ceiling(x)) == "x.ceil()"
    assert rust_code(floor(x)) == "x.floor()"

    # Automatic rewrite
    assert rust_code(Mod(x, 3)) == 'x - 3.0*((1_f64/3.0)*x).floor()'

