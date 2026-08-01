
def test_issue_11503():
    A = ReferenceFrame("A")
    A.orientnew("B", "Axis", [35, A.y])
    C = ReferenceFrame("C")
    A.orient(C, "Axis", [70, C.z])

