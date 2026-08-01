
def test_flat_element_deletion():
    it = np.ones(3).flat
    try:
        del it[1]
        del it[1:2]
    except TypeError:
        pass
    except Exception:
        raise AssertionError

