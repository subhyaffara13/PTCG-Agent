
def test_normalize_kwarg_pie():
    fig, ax = plt.subplots()
    x = [0.3, 0.3, 0.1]
    t1 = ax.pie(x=x, normalize=True)
    assert abs(t1[0][-1].theta2 - 360.) < 1e-3
    t2 = ax.pie(x=x, normalize=False)
    assert abs(t2[0][-1].theta2 - 360.) > 1e-3

