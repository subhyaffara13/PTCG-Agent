
def same_content(ref, test, endswith=False):
    """Is the content of two cells the same, up to reformatting by black"""
    ref = black_invariant(ref)
    test = black_invariant(test)

    if endswith and test:
        return ref.endswith(test)
    return ref == test


def same_content(ref_source, test_source, allow_removed_final_blank_line):
    """Is the content of two cells the same, except for an optional final blank line?"""
    if ref_source == test_source:
        return True

    if not allow_removed_final_blank_line:
        return False

    # Is ref identical to test, plus one blank line?
    ref_source = ref_source.splitlines()
    test_source = test_source.splitlines()

    if not ref_source:
        return False

    if ref_source[:-1] != test_source:
        return False

    return _BLANK_LINE.match(ref_source[-1])

