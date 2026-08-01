
def test_operator_object_right(o, op, type_):
    try:
        with recursionlimit(200):
            op(type_(1), o)
    except TypeError:
        pass

