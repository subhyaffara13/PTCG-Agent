
def test_implementation_details():
    lst = [39, 43, 92, 49, 22, 29, 93, 98, 26, 57, 8]
    tup = tuple(lst)
    assert m.sequence_item_get_ssize_t(lst) == 43
    assert m.sequence_item_set_ssize_t(lst) is None
    assert lst[1] == "peppa"
    assert m.sequence_item_get_size_t(lst) == 92
    assert m.sequence_item_set_size_t(lst) is None
    assert lst[2] == "george"
    assert m.list_item_get_ssize_t(lst) == 49
    assert m.list_item_set_ssize_t(lst) is None
    assert lst[3] == "rebecca"
    assert m.list_item_get_size_t(lst) == 22
    assert m.list_item_set_size_t(lst) is None
    assert lst[4] == "richard"
    assert m.tuple_item_get_ssize_t(tup) == 29
    assert m.tuple_item_set_ssize_t() == ("emely", "edmond")
    assert m.tuple_item_get_size_t(tup) == 93
    assert m.tuple_item_set_size_t() == ("candy", "cat")

