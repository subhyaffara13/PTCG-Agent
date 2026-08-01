
def test_iter_element_deletion():
    it = np.nditer(np.ones(3))
    try:
        del it[1]
        del it[1:2]
    except TypeError:
        pass
    except Exception:
        raise AssertionError

