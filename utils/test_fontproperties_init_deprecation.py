
def test_fontproperties_init_deprecation():
    """
    Test the deprecated API of FontProperties.__init__.

    The deprecation does not change behavior, it only adds a deprecation warning
    via a decorator. Therefore, the purpose of this test is limited to check
    which calls do and do not issue deprecation warnings. Behavior is still
    tested via the existing regular tests.
    """
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        # multiple positional arguments
        FontProperties("Times", "italic")

    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        # Mixed positional and keyword arguments
        FontProperties("Times", size=10)

    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        # passing a family list positionally
        FontProperties(["Times"])

    # still accepted:
    FontProperties(family="Times", style="italic")
    FontProperties(family="Times")
    FontProperties("Times")  # works as pattern and family
    FontProperties("serif-24:style=oblique:weight=bold")  # pattern

    # also still accepted:
    # passing as pattern via family kwarg was not covered by the docs but
    # historically worked. This is left unchanged for now.
    # AFAICT, we cannot detect this: We can determine whether a string
    # works as pattern, but that doesn't help, because there are strings
    # that are both pattern and family. We would need to identify, whether
    # a string is *not* a valid family.
    # Since this case is not covered by docs, I've refrained from jumping
    # extra hoops to detect this possible API misuse.
    FontProperties(family="serif-24:style=oblique:weight=bold")

