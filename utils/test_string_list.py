
def test_string_list():
    lst = m.StringList()
    lst.push_back("Element 1")
    lst.push_back("Element 2")
    assert m.print_opaque_list(lst) == "Opaque list: [Element 1, Element 2]"
    assert lst.back() == "Element 2"

    for i, k in enumerate(lst, start=1):
        assert k == f"Element {i}"
    lst.pop_back()
    assert m.print_opaque_list(lst) == "Opaque list: [Element 1]"

    cvp = m.ClassWithSTLVecProperty()
    assert m.print_opaque_list(cvp.stringList) == "Opaque list: []"

    cvp.stringList = lst
    cvp.stringList.push_back("Element 3")
    assert m.print_opaque_list(cvp.stringList) == "Opaque list: [Element 1, Element 3]"

