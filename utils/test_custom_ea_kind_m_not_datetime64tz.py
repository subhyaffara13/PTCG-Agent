
def test_custom_ea_kind_M_not_datetime64tz():
    # GH 34986
    class NotTZDtype(ExtensionDtype):
        @property
        def kind(self) -> str:
            return "M"

    not_tz_dtype = NotTZDtype()
    msg = "is_datetime64tz_dtype is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        assert not com.is_datetime64tz_dtype(not_tz_dtype)
        assert not com.needs_i8_conversion(not_tz_dtype)

