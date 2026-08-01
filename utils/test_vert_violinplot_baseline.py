
def test_vert_violinplot_baseline():
    # First 9 digits of frac(sqrt(2))
    np.random.seed(414213562)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax = plt.axes()
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False,
                  showmedians=False)

    # Reuse testcase from above for a labeled data test
    data = {"d": data}
    fig, ax = plt.subplots()
    ax.violinplot("d", positions=range(4), showmeans=False, showextrema=False,
                  showmedians=False, data=data)

