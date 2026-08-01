
def test_enum_pickle():
    from pybind11_tests import enums as e

    data = pickle.dumps(e.EOne, 2)
    assert e.EOne == pickle.loads(data)

