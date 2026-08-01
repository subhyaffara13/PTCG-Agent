
def test_signature(doc):
    assert (
        doc(m.create_rec_nested)
        == "create_rec_nested(arg0: int) -> numpy.ndarray[NestedStruct]"
    )

