
def test_Array():
    arr = Array(range(10))
    assert latex(arr) == r'\left[\begin{matrix}0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9\end{matrix}\right]'

    arr = Array(range(11))
    # fill the empty argument with a bunch of 'c' to avoid latex errors
    assert latex(arr) == r'\left[\begin{array}{ccccccccccc}0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10\end{array}\right]'

