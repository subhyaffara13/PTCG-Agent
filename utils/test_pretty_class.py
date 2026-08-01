
def test_pretty_class():
    """Test that the printer dispatcher correctly handles classes."""
    class C:
        pass   # C has no .__class__ and this was causing problems

    class D:
        pass

    assert pretty( C ) == str( C )
    assert pretty( D ) == str( D )

