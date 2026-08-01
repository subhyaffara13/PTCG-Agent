
def test_css_side_shorthands(shorthand, expansions):
    top, right, bottom, left = expansions

    assert_resolves(
        f"{shorthand}: 1pt", {top: "1pt", right: "1pt", bottom: "1pt", left: "1pt"}
    )

    assert_resolves(
        f"{shorthand}: 1pt 4pt", {top: "1pt", right: "4pt", bottom: "1pt", left: "4pt"}
    )

    assert_resolves(
        f"{shorthand}: 1pt 4pt 2pt",
        {top: "1pt", right: "4pt", bottom: "2pt", left: "4pt"},
    )

    assert_resolves(
        f"{shorthand}: 1pt 4pt 2pt 0pt",
        {top: "1pt", right: "4pt", bottom: "2pt", left: "0pt"},
    )

    with tm.assert_produces_warning(CSSWarning, match="Could not expand"):
        assert_resolves(f"{shorthand}: 1pt 1pt 1pt 1pt 1pt", {})

