
def test_numpy_err_state_is_default():
    expected = {"over": "warn", "divide": "warn", "invalid": "warn", "under": "ignore"}
    import numpy as np

    # The error state should be unchanged after that import.
    assert np.geterr() == expected

