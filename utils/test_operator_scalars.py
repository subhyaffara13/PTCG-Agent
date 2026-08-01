
def test_operator_scalars(op, type1, type2):
    try:
        op(type1(1), type2(1))
    except TypeError:
        pass

