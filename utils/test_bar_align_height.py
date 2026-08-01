
def test_bar_align_height():
    # test when keyword height is used 'no-repeat center' and 'background-size' present
    data = DataFrame([[1], [2]])
    result = data.style.bar(align="left", height=50)._compute().ctx
    bg_s = "linear-gradient(90deg, #d65f5f 100.0%, transparent 100.0%) no-repeat center"
    expected = {
        (0, 0): [("width", "10em")],
        (1, 0): [
            ("width", "10em"),
            ("background", bg_s),
            ("background-size", "100% 50.0%"),
        ],
    }
    assert result == expected

