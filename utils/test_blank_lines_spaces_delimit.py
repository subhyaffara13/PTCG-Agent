
def test_blank_lines_spaces_delimit(ws):
    txt = StringIO(
        f"1 2{ws}30\n\n{ws}\n"
        f"4 5 60{ws}\n  {ws}  \n"
        f"7 8 {ws} 90\n  # comment\n"
        f"3 2 1"
    )
    # NOTE: It is unclear that the `  # comment` should succeed. Except
    #       for delimiter=None, which should use any whitespace (and maybe
    #       should just be implemented closer to Python
    expected = np.array([[1, 2, 30], [4, 5, 60], [7, 8, 90], [3, 2, 1]])
    assert_equal(
        np.loadtxt(txt, dtype=int, delimiter=None, comments="#"), expected
    )

