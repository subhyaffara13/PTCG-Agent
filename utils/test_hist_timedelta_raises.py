
def test_hist_timedelta_raises():
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    arr_np = np.array([1, 2, 5, 7], dtype="timedelta64[D]")
    with pytest.raises(TypeError, match="does not currently support timedelta inputs"):
        ax.hist(arr_np)

    arr_py = [datetime.timedelta(seconds=i) for i in range(5)]
    with pytest.raises(TypeError, match="does not currently support timedelta inputs"):
        ax.hist(arr_py)

