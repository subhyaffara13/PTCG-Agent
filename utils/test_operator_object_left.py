
def test_operator_object_left(o, op, type_):
    try:
        with recursionlimit(200):
            op(o, type_(1))
    except TypeError:
        pass

