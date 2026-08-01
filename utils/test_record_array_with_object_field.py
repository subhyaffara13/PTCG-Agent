
def test_record_array_with_object_field():
    # Trac #1839
    y = ma.masked_array(
        [(1, '2'), (3, '4')],
        mask=[(0, 0), (0, 1)],
        dtype=[('a', int), ('b', object)])
    # getting an item used to fail
    y[1]

