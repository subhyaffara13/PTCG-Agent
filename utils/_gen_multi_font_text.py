
def _gen_multi_font_text():
    """
    Generate text intended for use with multiple fonts to exercise font fallbacks.

    Returns
    -------
    fonts : list of str
        The names of the fonts used to render the test string, sorted by intended
        priority. This should be set as the font family for the Figure or Text artist.
    text : str
        The test string.
    """
    # These fonts are serif and sans-serif, and would not normally be combined, but that
    # should make it easier to see which glyph is from which font.
    fonts = ['cmr10', 'DejaVu Sans']
    # cmr10 does not contain accented characters, so they should fall back to DejaVu
    # Sans. However, some accented capital A versions *are* in cmr10 with non-standard
    # glyph shapes, so don't test those (otherwise this Latin1 supplement group would
    # start at 0xA0.)
    start = 0xC5
    latin1_supplement = [chr(x) for x in range(start, 0xFF+1)]
    latin_extended_A = [chr(x) for x in range(0x100, 0x17F+1)]
    latin_extended_B = [chr(x) for x in range(0x180, 0x24F+1)]
    non_basic_multilingual_plane = [chr(x) for x in range(0x1F600, 0x1F610)]
    count = itertools.count(start - 0xA0)
    non_basic_characters = '\n'.join(
        ''.join(line)
        for _, line in itertools.groupby(  # Replace with itertools.batched for Py3.12+.
            [*latin1_supplement, *latin_extended_A, *latin_extended_B,
             *non_basic_multilingual_plane],
            key=lambda x: next(count) // 32)  # 32 characters per line.
    )
    test_str = f"""There are basic characters
{string.ascii_uppercase} {string.ascii_lowercase}
{string.digits} {string.punctuation}
and accented characters
{non_basic_characters}
in between!"""
    # The resulting string contains 491 unique characters. Some file formats use 8-bit
    # tables, which the large number of characters exercises twice over.
    return fonts, test_str

