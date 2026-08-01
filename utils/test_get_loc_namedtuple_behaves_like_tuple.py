
def test_get_loc_namedtuple_behaves_like_tuple():
    # GH57922
    NamedIndex = namedtuple("NamedIndex", ("a", "b"))
    multi_idx = MultiIndex.from_tuples(
        [NamedIndex("i1", "i2"), NamedIndex("i3", "i4"), NamedIndex("i5", "i6")]
    )
    for idx in (multi_idx, multi_idx.to_flat_index()):
        assert idx.get_loc(NamedIndex("i1", "i2")) == 0
        assert idx.get_loc(NamedIndex("i3", "i4")) == 1
        assert idx.get_loc(NamedIndex("i5", "i6")) == 2
        assert idx.get_loc(("i1", "i2")) == 0
        assert idx.get_loc(("i3", "i4")) == 1
        assert idx.get_loc(("i5", "i6")) == 2
    multi_idx = MultiIndex.from_tuples([("i1", "i2"), ("i3", "i4"), ("i5", "i6")])
    for idx in (multi_idx, multi_idx.to_flat_index()):
        assert idx.get_loc(NamedIndex("i1", "i2")) == 0
        assert idx.get_loc(NamedIndex("i3", "i4")) == 1
        assert idx.get_loc(NamedIndex("i5", "i6")) == 2
        assert idx.get_loc(("i1", "i2")) == 0
        assert idx.get_loc(("i3", "i4")) == 1
        assert idx.get_loc(("i5", "i6")) == 2

