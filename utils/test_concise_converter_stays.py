
def test_concise_converter_stays():
    # This test demonstrates problems introduced by gh-23417 (reverted in gh-25278)
    # In particular, downstream libraries like Pandas had their designated converters
    # overridden by actions like setting xlim (or plotting additional points using
    # stdlib/numpy dates and string date representation, which otherwise work fine with
    # their date converters)
    # While this is a bit of a toy example that would be unusual to see it demonstrates
    # the same ideas (namely having a valid converter already applied that is desired)
    # without introducing additional subclasses.
    # See also discussion at gh-25219 for how Pandas was affected
    x = [datetime.datetime(2000, 1, 1), datetime.datetime(2020, 2, 20)]
    y = [0, 1]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # Bypass Switchable date converter
    conv = mdates.ConciseDateConverter()
    with pytest.warns(UserWarning, match="already has a converter"):
        ax.xaxis.set_converter(conv)
    assert ax.xaxis.units is None
    ax.set_xlim(*x)
    assert ax.xaxis.get_converter() == conv

