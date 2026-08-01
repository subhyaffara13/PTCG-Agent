
def test_orientnew_respects_parent_class():
    class MyReferenceFrame(ReferenceFrame):
        pass
    B = MyReferenceFrame('B')
    C = B.orientnew('C', 'Axis', [0, B.x])
    assert isinstance(C, MyReferenceFrame)

