
def test_enum_to_int():
    m.test_enum_to_int(m.Flags.Read)
    m.test_enum_to_int(m.ClassWithUnscopedEnum.EMode.EFirstMode)
    m.test_enum_to_int(m.ScopedCharEnum.Positive)
    m.test_enum_to_int(m.ScopedBoolEnum.TRUE)
    m.test_enum_to_uint(m.Flags.Read)
    m.test_enum_to_uint(m.ClassWithUnscopedEnum.EMode.EFirstMode)
    m.test_enum_to_uint(m.ScopedCharEnum.Positive)
    m.test_enum_to_uint(m.ScopedBoolEnum.TRUE)
    m.test_enum_to_long_long(m.Flags.Read)
    m.test_enum_to_long_long(m.ClassWithUnscopedEnum.EMode.EFirstMode)
    m.test_enum_to_long_long(m.ScopedCharEnum.Positive)
    m.test_enum_to_long_long(m.ScopedBoolEnum.TRUE)

