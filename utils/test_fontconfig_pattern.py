
def test_fontconfig_pattern():
    """Test converting a FontProperties to string then back."""

    # Defaults
    test = "defaults "
    f1 = FontProperties()
    s = str(f1)

    f2 = FontProperties(s)
    for k in keys:
        assert getattr(f1, k)() == getattr(f2, k)(), test + k

    # Basic inputs
    test = "basic "
    f1 = FontProperties(family="serif", size=20, style="italic")
    s = str(f1)

    f2 = FontProperties(s)
    for k in keys:
        assert getattr(f1, k)() == getattr(f2, k)(), test + k

    # Full set of inputs.
    test = "full "
    f1 = FontProperties(family="sans-serif", size=24, weight="bold",
                        style="oblique", variant="small-caps",
                        stretch="expanded")
    s = str(f1)

    f2 = FontProperties(s)
    for k in keys:
        assert getattr(f1, k)() == getattr(f2, k)(), test + k

