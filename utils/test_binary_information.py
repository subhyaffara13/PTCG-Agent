
def test_binary_information():
    assert convert_to(kibibyte, byte) == 1024*byte
    assert convert_to(mebibyte, byte) == 1024**2*byte
    assert convert_to(gibibyte, byte) == 1024**3*byte
    assert convert_to(tebibyte, byte) == 1024**4*byte
    assert convert_to(pebibyte, byte) == 1024**5*byte
    assert convert_to(exbibyte, byte) == 1024**6*byte

    assert kibibyte.convert_to(bit) == 8*1024*bit
    assert byte.convert_to(bit) == 8*bit

    a = 10*kibibyte*hour

    assert convert_to(a, byte) == 10240*byte*hour
    assert convert_to(a, minute) == 600*kibibyte*minute
    assert convert_to(a, [byte, minute]) == 614400*byte*minute

