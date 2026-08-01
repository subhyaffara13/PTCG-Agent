
def simple_frame():
    """
    Fixture for simple 3x3 DataFrame

    Columns are ['one', 'two', 'three'], index is ['a', 'b', 'c'].

       one  two  three
    a  1.0  2.0    3.0
    b  4.0  5.0    6.0
    c  7.0  8.0    9.0
    """
    arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])

    return DataFrame(arr, columns=["one", "two", "three"], index=["a", "b", "c"])

