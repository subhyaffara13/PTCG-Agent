
def test_docstring_signatures():
    for enum_type in [m.ScopedEnum, m.UnscopedEnum]:
        for attr in enum_type.__dict__.values():
            # Issue #2623/PR #2637: Add argument names to enum_ methods
            assert "arg0" not in (attr.__doc__ or "")

