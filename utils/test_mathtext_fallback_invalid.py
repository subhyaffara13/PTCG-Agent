
def test_mathtext_fallback_invalid():
    for fallback in ['abc', '']:
        with pytest.raises(ValueError, match="not a valid fallback font name"):
            mpl.rcParams['mathtext.fallback'] = fallback

