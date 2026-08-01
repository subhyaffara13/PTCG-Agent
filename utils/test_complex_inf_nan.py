
def test_complex_inf_nan(dtype):
    """Check inf/nan formatting of complex types."""
    TESTS = {
        complex(np.inf, 0): "(inf+0j)",
        complex(0, np.inf): "infj",
        complex(-np.inf, 0): "(-inf+0j)",
        complex(0, -np.inf): "-infj",
        complex(np.inf, 1): "(inf+1j)",
        complex(1, np.inf): "(1+infj)",
        complex(-np.inf, 1): "(-inf+1j)",
        complex(1, -np.inf): "(1-infj)",
        complex(np.nan, 0): "(nan+0j)",
        complex(0, np.nan): "nanj",
        complex(-np.nan, 0): "(nan+0j)",
        complex(0, -np.nan): "nanj",
        complex(np.nan, 1): "(nan+1j)",
        complex(1, np.nan): "(1+nanj)",
        complex(-np.nan, 1): "(nan+1j)",
        complex(1, -np.nan): "(1+nanj)",
    }
    for c, s in TESTS.items():
        assert_equal(str(dtype(c)), s)

