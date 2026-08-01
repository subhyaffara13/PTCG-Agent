
def test_save_object():
    class C:
        pass
    c = C()
    c.field1 = 1
    c.field2 = 'a string'
    stream = BytesIO()
    savemat(stream, {'c': c})
    d = loadmat(stream, struct_as_record=False)
    c2 = d['c'][0,0]
    assert_equal(c2.field1, 1)
    assert_equal(c2.field2, 'a string')
    d = loadmat(stream, struct_as_record=True)
    c2 = d['c'][0,0]
    assert_equal(c2['field1'], 1)
    assert_equal(c2['field2'], 'a string')

