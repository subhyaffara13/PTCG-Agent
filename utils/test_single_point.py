
def test_single_point():
    # Issue #1796: don't let lines.marker affect the grid
    matplotlib.rcParams['lines.marker'] = 'o'
    matplotlib.rcParams['axes.grid'] = True

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot([0], [0], 'o')
    ax2.plot([1], [1], 'o')

    # Reuse testcase from above for a labeled data test
    data = {'a': [0], 'b': [1]}

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot('a', 'a', 'o', data=data)
    ax2.plot('b', 'b', 'o', data=data)

