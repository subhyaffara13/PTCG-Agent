
def test_looped_frame_warning():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    C = ReferenceFrame('C')

    a, b, c = symbols('a b c')
    B.orient_axis(A, A.x, a)
    C.orient_axis(B, B.x, b)

    with warnings.catch_warnings(record = True) as w:
        warnings.simplefilter("always")
        A.orient_axis(C, C.x, c)
        assert issubclass(w[-1].category, UserWarning)
        assert 'Loops are defined among the orientation of frames. ' + \
            'This is likely not desired and may cause errors in your calculations.' in str(w[-1].message)

