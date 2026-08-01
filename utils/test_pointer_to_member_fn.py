
def test_pointer_to_member_fn():
    for cls in [m.Buffer, m.ConstBuffer, m.DerivedBuffer]:
        buf = cls()
        buf.value = 0x12345678
        value = struct.unpack("i", bytearray(buf))[0]
        assert value == 0x12345678

