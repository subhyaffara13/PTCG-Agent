
def test_boxplot():
    # Randomness used for bootstrapping.
    np.random.seed(937)

    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()

    ax.boxplot([x, x], bootstrap=10000, notch=1)
    ax.set_ylim(-30, 30)

    # Reuse testcase from above for a labeled data test
    data = {"x": [x, x]}
    fig, ax = plt.subplots()
    ax.boxplot("x", bootstrap=10000, notch=1, data=data)
    ax.set_ylim(-30, 30)

